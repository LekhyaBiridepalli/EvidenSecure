import hashlib
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .db import *  # Import the MongoDB connection
from .utils import *





# Create your views here.
def home(request):
    return render(request, 'evidence/index.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['logemail']
#         password = request.POST['logpass']

#         # Authenticate the user
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')  # Redirect to a home or dashboard page after login
#         else:
#             messages.error(request, 'Invalid credentials. Please try again.')
#             return render(request, 'evidence/login.html')

#     return render(request, 'evidence/login.html')
def login_view(request):
    if request.method == 'POST':
        # Bypass authentication for testing purposes
        return redirect('dashboard')  # Directly redirect to the dashboard page
    
    return render(request, 'evidence/login.html')

# View for the signup page
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can log in now!')
            return redirect('login')  # Redirect to login page after successful signup
        else:
            messages.error(request, 'There was an error. Please try again.')
            return render(request, 'evidence/signup.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'evidence/signup.html', {'form': form})

# View for logging out the user
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the login page after logout

def dashboard(request):
    return render(request, 'evidence/dashboard.html')

def cases(request):
    # You can pass any context data related to cases here if needed
    return render(request, 'evidence/cases.html')

# Evidence Management View
def evidence(request):
    # You can pass any context data related to cases here if needed
    return render(request, 'evidence/evidence.html')


from bson import ObjectId
from datetime import datetime, timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json

def add_case(request):
    if request.method == 'POST':
        try:
            # Capture form data
            case_type = request.POST.get('case_type')
            case_date = request.POST.get('case_date')
            investigating_officer = request.POST.get('investigating_officer')
            case_status = request.POST.get('case_status')
            accused_names = request.POST.getlist('accused_names')  # Get multiple accused names
            victim_names = request.POST.getlist('victim_names')  # Get multiple victim names
            court_case_number = request.POST.get('court_case_number', '')
            remarks = request.POST.get('remarks', '')
            charges = request.POST.getlist('charges')  # Get multiple charges

            # Validate required fields
            if not case_type or not case_date or not investigating_officer or not case_status:
                return JsonResponse({"error": "Missing required fields: case_type, case_date, investigating_officer, case_status"}, status=400)

            # Convert case_date to datetime
            try:
                case_date = datetime.strptime(case_date, "%Y-%m-%d")
            except ValueError:
                return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

            # Generate a new case_id as ObjectId
            case_id = ObjectId()  # This will create a valid ObjectId

            # Prepare the new case data
            new_case = {
                "case_id": case_id,  # case_id should be ObjectId
                "case_type": case_type,
                "case_date": case_date,
                "investigating_officer": investigating_officer,
                "case_status": case_status,
                "accused_names": accused_names,  # Store as a list
                "victim_names": victim_names,  # Store as a list
                "court_case_number": court_case_number,
                "remarks": remarks,
                "charges": charges  # Store as a list
            }

            # Insert the case into MongoDB
            result = cases_collection.insert_one(new_case)

            # Redirect to the case list or show a success message
            return redirect('cases')  # Or return a success message as you see fit

        except Exception as e:
            # Handle any errors and send back a response
            return JsonResponse({"error": str(e)}, status=500)

    # If method is GET, render the add_case form
    return render(request, 'evidence/add_case.html')



def case_detail(request, case_id):
    # Fetch the case details using ObjectId
    try:
        case = cases_collection.find_one({"_id": ObjectId(case_id)})
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=400)
    
    if not case:
        return HttpResponse("Case not found", status=404)

    # Convert ObjectId to string for display
    case["id"] = str(case["_id"])
    case["case_date"] = case["case_date"].strftime('%Y-%m-%d')  # Format the date as string

    return render(request, "evidence/case_detail.html", {"case": case})


def cases(request):
    search_results = []
    
    # If there is a query in the search input
    query = request.GET.get('query', '')
    
    # If the search query exists, filter cases based on the query
    if query:
        search_results = cases_collection.find({
            "$or": [
                {"case_type": {"$regex": query, "$options": "i"}},  # Search in case_type
                {"accused_names": {"$regex": query, "$options": "i"}},  # Search in accused_names
                {"victim_names": {"$regex": query, "$options": "i"}}  # Search in victim_names
            ]
        })
    else:
        # Fetch all cases if no search query is provided
        search_results = cases_collection.find()

    all_cases = cases_collection.find()
    all_cases = [{**case, "case_id": str(case["_id"])} for case in all_cases]
    search_results = [{**case, "case_id": str(case["_id"])} for case in search_results]

    return render(request, 'evidence/cases.html', { 'all_cases': all_cases,'search_results': search_results })


from django.shortcuts import render, redirect
from django.conf import settings
from pymongo import MongoClient
from bson import ObjectId
import gridfs
import os

from django.core.files.uploadedfile import InMemoryUploadedFile


# def evidence_view(request):
#     # Get the court_case_number from GET request
#     court_case_number = request.GET.get('court_case_number', '')

#     # Get the case from the database using the court_case_number
#     case = get_case_by_number(court_case_number)
    
#     if case:
#         # If the case exists, find the evidence linked to this case
#         evidence_list = get_evidence_by_case_id(case['_id'])
#     else:
#         evidence_list = []
    
#     return render(request, 'evidence/evidence.html', {
#         'court_case_number': court_case_number,  # Pass court_case_number to the template
#         'evidence_list': evidence_list,  # Pass the evidence list to the template
#     })

# from django.core.files.storage import FileSystemStorage
# from django.utils import timezone


# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from pymongo import MongoClient
# import gridfs
# from django.utils import timezone

# fs = gridfs.GridFS(db)



import logging
# # # Initialize logger
logger = logging.getLogger(__name__)

# # def add_evidence(request):
# #     if request.method == 'POST':
# #         # Get the court case number input from the form
# #         court_case_number = request.POST.get('court_case_number')

# #         # Retrieve the case object by case number
# #         case = get_case_by_number(court_case_number)
        
# #         if case:
# #             # Extract case_id from the case object
# #             case_id = case.get('_id')  # or 'id' depending on your MongoDB setup

# #             # Now extract other form data
# #             evidence_type = request.POST.get('evidence_type')
# #             evidence_description = request.POST.get('evidence_description')
# #             collected_by = request.POST.get('collected_by')
# #             remarks = request.POST.get('remarks', '')  # Optional field
# #             upload_date = timezone.now()  # Use current timestamp for upload date

# #             # Handle file upload
# #             print(request.FILES.get('file'))

# #             uploaded_file = request.FILES.get('file')

# # # Debugging: Check if the file object is retrieved
# #             if uploaded_file:
# #                 print(f"File Name: {uploaded_file.name}")
# #                 print(f"File Size: {uploaded_file.size} bytes")
# #                 print(f"File Type: {uploaded_file.content_type}")
# #             else:
# #                 print("No file uploaded.")


# #             if uploaded_file:
# #                 try:
# #                     # Save the file to GridFS
# #                     # Save the file to GridFS
# #                     file_id = fs.put(uploaded_file.read(), filename=uploaded_file.name, content_type=uploaded_file.content_type)

# #                     print(f"File saved with ID: {file_id}")

# #                     file_type = uploaded_file.content_type  # Extract file type (e.g., image/jpeg)
# #                     file_name = uploaded_file.name  # Original file name
# #                     file_size = uploaded_file.size  # File size in bytes

# #                     # Log the file upload info
# #                     logger.info(f"File uploaded: {file_name}, file_id: {file_id}")

# #                     # Construct the files array as required by the schema
# #                     files = [{
# #                         'file_id': file_id,
# #                         'file_type': file_type,
# #                         'file_name': file_name,
# #                         'file_size': file_size
# #                     }]
# #                 except Exception as e:
# #                     logger.error(f"Error saving file: {str(e)}")
# #                     return HttpResponse(f"Error saving file: {str(e)}", status=500)
# #             else:
# #                 files = [] 
# #                 print("No file uploaded") # No file uploaded

# #             # Create the evidence document to be inserted into MongoDB
# #             new_evidence = {
# #                 'case_id': case_id,
# #                 'evidence_type': evidence_type,
# #                 'evidence_description': evidence_description,
# #                 'collected_by': collected_by,
# #                 'upload_date': upload_date,
# #                 'remarks': remarks,
# #                 'files': files  # Reference to files in GridFS
# #             }

# #             # Insert the document into the evidence collection
# #             try:
# #                 evidence_collection.insert_one(new_evidence)
# #                 return redirect('evidence')  # Redirect to the evidence management page or success page
# #             except Exception as e:
# #                 logger.error(f"Error inserting evidence into database: {str(e)}")
# #                 return HttpResponse(f"Error inserting evidence into database: {str(e)}", status=500)

# #         else:
# #             # Case not found
# #             logger.warning(f"Case not found for court case number: {court_case_number}")
# #             return HttpResponse("Case not found", status=404)

# #     return render(request, 'evidence/add_evidence.html')

# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# import os
# from base64 import b64encode

# # Key and IV should ideally be stored securely, not hard-coded.
# key = os.urandom(32)  # 256-bit key for AES
# iv = os.urandom(16)   # 128-bit IV

# def encrypt_data(data):
#     # Pad the data to make it a multiple of block size
#     padder = padding.PKCS7(algorithms.AES.block_size).padder()
#     padded_data = padder.update(data.encode()) + padder.finalize()

#     # Encrypt the padded data
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     encryptor = cipher.encryptor()
#     encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

#     # Return encrypted data in base64 encoding for storage in MongoDB
#     return b64encode(encrypted_data).decode()

# def add_evidence(request):
#     if request.method == 'POST':
#         # Get the court case number input from the form
#         court_case_number = request.POST.get('court_case_number')

#         # Retrieve the case object by case number
#         case = get_case_by_number(court_case_number)
        
#         if case:
#             # Extract case_id from the case object
#             case_id = case.get('_id')

#             # Extract other form data
#             evidence_type = request.POST.get('evidence_type')
#             evidence_description = request.POST.get('evidence_description')
#             collected_by = request.POST.get('collected_by')
#             remarks = request.POST.get('remarks', '')  # Optional field
#             upload_date = timezone.now()  # Use current timestamp for upload date

#             # Encrypt the evidence description
#             encrypted_description = encrypt_data(evidence_description)

#             # Handle file upload
#             uploaded_file = request.FILES.get('file')

#             if uploaded_file:
#                 try:
#                     # Save the file to GridFS
#                     file_id = fs.put(uploaded_file.read(), filename=uploaded_file.name, content_type=uploaded_file.content_type)

#                     file_type = uploaded_file.content_type
#                     file_name = uploaded_file.name
#                     file_size = uploaded_file.size

#                     # Construct the files array as required by the schema
#                     files = [{
#                         'file_id': file_id,
#                         'file_type': file_type,
#                         'file_name': file_name,
#                         'file_size': file_size
#                     }]
#                 except Exception as e:
#                     return HttpResponse(f"Error saving file: {str(e)}", status=500)
#             else:
#                 files = [] 

#             # Create the evidence document to be inserted into MongoDB
#             new_evidence = {
#                 'case_id': case_id,
#                 'evidence_type': evidence_type,
#                 'evidence_description': encrypted_description,  # Store encrypted description
#                 'collected_by': collected_by,
#                 'upload_date': upload_date,
#                 'remarks': remarks,
#                 'files': files
#             }

#             try:
#                 evidence_collection.insert_one(new_evidence)
#                 return redirect('evidence')  # Redirect to the evidence management page or success page
#             except Exception as e:
#                 return HttpResponse(f"Error inserting evidence into database: {str(e)}", status=500)

#         else:
#             return HttpResponse("Case not found", status=404)

#     return render(request, 'evidence/add_evidence.html')


# from bson import ObjectId


    

# def view_file(request, file_id):
#     try:
#         if isinstance(file_id, str):
#              file_id = ObjectId(file_id)
#         # Ensure file_id is being correctly parsed
#         print(f"Retrieving file with ID: {file_id}")
        
        
#         # Try to get the file from GridFS using the file_id
#         file = fs.get(file_id)
#         print(f"File retrieved: {file.filename}")
#         print(f"File Type: {file.content_type}")

        
#         response = HttpResponse(file, content_type=file.content_type)
        
#         # Handle file types for displaying in the browser
#         if file.content_type.startswith('image'):
#             response['Content-Type'] = file.content_type
#         elif file.content_type == 'application/pdf':
#             response['Content-Type'] = 'application/pdf'
#         elif file.content_type == 'text/plain':
#             response['Content-Type'] = 'text/plain'  # Handle plain text
#         else:
#             response['Content-Type'] = 'application/octet-stream'  # For generic files
#         CHUNK_SIZE = 8192  # 8 KB chunks
#         with file as f:
#             for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
#                 response.write(chunk)
        
#         return response
    
#     except gridfs.errors.NoFile:
#         print(f"File with ID {file_id} not found.")
#         return HttpResponse("File not found", status=404)

# def decrypt_data(encrypted_data):
#     # Decode the base64 encoded encrypted data
#     encrypted_data = b64decode(encrypted_data)

#     # Decrypt the data
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     decryptor = cipher.decryptor()
#     decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

#     # Unpad the decrypted data
#     unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
#     unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

#     # Return decrypted data as a string
#     return unpadded_data.decode()

# def view_file(request, file_id):
#     try:
#         if isinstance(file_id, str):
#              file_id = ObjectId(file_id)

#         # Retrieve the file from GridFS
#         file = fs.get(file_id)

#         # If you have an encrypted file or document, decrypt it
#         evidence_description = file.get('evidence_description', None)
#         if evidence_description:
#             decrypted_description = decrypt_data(evidence_description)
#             file['evidence_description'] = decrypted_description

#         response = HttpResponse(file, content_type=file.content_type)

#         return response

#     except gridfs.errors.NoFile:
#         return HttpResponse("File not found", status=404)


# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.core.files.storage import default_storage
# from .utils import encrypt_data, encrypt_file, save_encrypted_evidence

# # View for adding evidence
# def add_evidence(request):
#     if request.method == 'POST':
#         case_id = request.POST['case_id']
#         evidence_type = request.POST['evidence_type']
#         evidence_description = request.POST['evidence_description']
#         collected_by = request.POST['collected_by']
        
#         evidence_file = request.FILES['file'] if 'file' in request.FILES else None
        
#         # Encrypt the data
#         encrypted_evidence_type = encrypt_data(evidence_type)
#         encrypted_evidence_description = encrypt_data(evidence_description)
#         encrypted_collected_by = encrypt_data(collected_by)

#         if evidence_file:
#             file_data = evidence_file.read()
#             encrypted_file_data = encrypt_file(file_data)

#             # Save the encrypted evidence and file to MongoDB and GridFS
#             save_encrypted_evidence(
#                 case_id=case_id,
#                 evidence_type=encrypted_evidence_type,
#                 evidence_description=encrypted_evidence_description,
#                 collected_by=encrypted_collected_by,
#                 file_data=encrypted_file_data,
#                 file_name=evidence_file.name,
#                 file_type=evidence_file.content_type
#             )
#             return JsonResponse({'status': 'success', 'message': 'Evidence added successfully'})

#     return render(request, 'add_evidence.html')

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from django.utils.crypto import get_random_string
import base64
from django.utils import timezone

# Key for AES encryption (for demonstration, use a secure method to store/retrieve keys)
SECRET_KEY = b'YourSecureKeyHere'  # 16 bytes for AES-128 (or 32 bytes for AES-256)

# Function to encrypt content using AES encryption
# def encrypt_content(content):
#     # Create a random 16-byte IV for AES CBC mode
#     iv = get_random_string(16).encode()
#     cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
#     padder = padding.PKCS7(128).padder()
#     padded_data = padder.update(content.encode()) + padder.finalize()
#     encryptor = cipher.encryptor()
#     encrypted_content = encryptor.update(padded_data) + encryptor.finalize()
#     return base64.b64encode(iv + encrypted_content).decode()  # Store iv and encrypted content as base64

# Function to decrypt content using AES decryption
# def decrypt_content(encrypted_content):
#     # Decode the base64 content
#     encrypted_content = base64.b64decode(encrypted_content)
#     iv = encrypted_content[:16]  # Extract the IV
#     encrypted_data = encrypted_content[16:]  # Extract the encrypted data

#     cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
#     decryptor = cipher.decryptor()
#     decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
#     unpadder = padding.PKCS7(128).unpadder()
#     decrypted_content = unpadder.update(decrypted_padded_data) + unpadder.finalize()
#     return decrypted_content.decode()

# Modify the add_evidence view to encrypt content before saving
# def add_evidence(request):
#     if request.method == 'POST':
#         court_case_number = request.POST.get('court_case_number')
#         case = get_case_by_number(court_case_number)
        
#         if case:
#             case_id = case.get('_id')

#             # Extract form data
#             evidence_type = encrypt_content(request.POST.get('evidence_type', ''))
#             evidence_description = encrypt_content(request.POST.get('evidence_description', ''))
#             collected_by = encrypt_content(request.POST.get('collected_by', ''))
#             remarks = encrypt_content(request.POST.get('remarks', ''))
#             upload_date = timezone.now()

#             # Handle file upload
#             uploaded_file = request.FILES.get('file')
#             files = []

#             if uploaded_file:
#                 try:
#                     file_id = fs.put(uploaded_file.read(), filename=uploaded_file.name, content_type=uploaded_file.content_type)
#                     file_type = uploaded_file.content_type
#                     file_name = uploaded_file.name
#                     file_size = uploaded_file.size

#                     # Encrypt the file content
#                     encrypted_file = encrypt_content(uploaded_file.read().decode('utf-8'))

#                     files = [{
#                         'file_id': file_id,
#                         'file_type': file_type,
#                         'file_name': file_name,
#                         'file_size': file_size,
#                         'encrypted_file': encrypted_file  # Store the encrypted file content
#                     }]
#                 except Exception as e:
#                     logger.error(f"Error saving file: {str(e)}")
#                     return HttpResponse(f"Error saving file: {str(e)}", status=500)

#             # Prepare the evidence document
#             new_evidence = {
#                 'case_id': case_id,
#                 'evidence_type': evidence_type,
#                 'evidence_description': evidence_description,
#                 'collected_by': collected_by,
#                 'upload_date': upload_date,
#                 'remarks': remarks,
#                 'files': files
#             }

#             # Insert evidence into MongoDB
#             try:
#                 evidence_collection.insert_one(new_evidence)
#                 return redirect('evidence')
#             except Exception as e:
#                 logger.error(f"Error inserting evidence: {str(e)}")
#                 return HttpResponse(f"Error inserting evidence: {str(e)}", status=500)
#         else:
#             return HttpResponse("Case not found", status=404)

#     return render(request, 'evidence/add_evidence.html')

# def add_evidence(request):
#     if request.method == 'POST':
#         court_case_number = request.POST.get('court_case_number')
#         case = get_case_by_number(court_case_number)

#         if case:
#             case_id = case.get('_id')

#             # Extract and encrypt form data
#             evidence_type = encrypt_content(request.POST.get('evidence_type', ''))
#             evidence_description = encrypt_content(request.POST.get('evidence_description', ''))
#             collected_by = encrypt_content(request.POST.get('collected_by', ''))
#             remarks = encrypt_content(request.POST.get('remarks', ''))
#             upload_date = timezone.now()

#             # Handle file upload
#             uploaded_file = request.FILES.get('file')
#             files = []

#             if uploaded_file:
#                 try:
#                     file_id = fs.put(uploaded_file.read(), filename=uploaded_file.name, content_type=uploaded_file.content_type)
#                     file_type = uploaded_file.content_type
#                     file_name = uploaded_file.name
#                     file_size = uploaded_file.size

#                     # Encrypt the file content
#                     encrypted_file = encrypt_content(uploaded_file.read().decode('utf-8'))

#                     files = [{
#                         'file_id': file_id,
#                         'file_type': file_type,
#                         'file_name': file_name,
#                         'file_size': file_size,
#                         'encrypted_file': encrypted_file  # Store the encrypted file content
#                     }]
#                 except Exception as e:
#                     logger.error(f"Error saving file: {str(e)}")
#                     return HttpResponse(f"Error saving file: {str(e)}", status=500)

#             # Prepare and insert evidence
#             new_evidence = {
#                 'case_id': case_id,
#                 'evidence_type': evidence_type,
#                 'evidence_description': evidence_description,
#                 'collected_by': collected_by,
#                 'upload_date': upload_date,
#                 'remarks': remarks,
#                 'files': files
#             }

#             try:
#                 evidence_collection.insert_one(new_evidence)
#                 return redirect('evidence')
#             except Exception as e:
#                 logger.error(f"Error inserting evidence: {str(e)}")
#                 return HttpResponse(f"Error inserting evidence: {str(e)}", status=500)
#         else:
#             return HttpResponse("Case not found", status=404)

#     return render(request, 'evidence/add_evidence.html')

# # Modify the view for file retrieval to decrypt the content
# def view_file(request, file_id):
#     try:
#         if isinstance(file_id, str):
#             file_id = ObjectId(file_id)

#         file = fs.get(file_id)

#         # Decrypt the file content
#         decrypted_content = decrypt_content(file.read().decode('utf-8'))
        
#         response = HttpResponse(decrypted_content, content_type=file.content_type)
        
#         if file.content_type.startswith('image'):
#             response['Content-Type'] = file.content_type
#         elif file.content_type == 'application/pdf':
#             response['Content-Type'] = 'application/pdf'
#         elif file.content_type == 'text/plain':
#             response['Content-Type'] = 'text/plain'
#         else:
#             response['Content-Type'] = 'application/octet-stream'

#         return response
#     except gridfs.errors.NoFile:
#         return HttpResponse("File not found", status=404)
#     except Exception as e:
#         return HttpResponse(f"Error retrieving file: {str(e)}", status=500)

# def decrypt_data(encrypted_data):
#     # Ensure the key is 256 bits (32 bytes)
#     key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()  # Hash the SECRET_KEY to get a 256-bit key
#     iv = encrypted_data[:16]  # Assuming the IV is the first 16 bytes of the encrypted data
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     decryptor = cipher.decryptor()
#     decrypted_data = decryptor.update(encrypted_data[16:]) + decryptor.finalize()
#     return decrypted_data.decode('utf-8')  # Returning as a string

# # def evidence_view(request):
# #     # Get the court_case_number from GET request
# #     court_case_number = request.GET.get('court_case_number', '')

# #     # Get the case from the database using the court_case_number
# #     case = get_case_by_number(court_case_number)
    
# #     if case:
# #         # If the case exists, find the evidence linked to this case
# #         evidence_list = get_evidence_by_case_id(case['_id'])
        
# #         # Decrypt sensitive fields for each evidence
# #         for evidence in evidence_list:
# #             # Decrypt text fields
# #             if 'evidence_description' in evidence:
# #                 evidence['evidence_description'] = decrypt_data(evidence['evidence_description'])
# #             if 'remarks' in evidence:
# #                 evidence['remarks'] = decrypt_data(evidence['remarks'])
            
# #             # Decrypt files if necessary
# #             if 'files' in evidence:
# #                 for file in evidence['files']:
# #                     # Fetch file from GridFS and decrypt the content
# #                     file_id = file['file_id']
# #                     file_data = fs.get(file_id).read()  # Retrieve file content from GridFS
# #                     decrypted_file_data = decrypt_data(file_data)  # Decrypt the file data
# #                     file['decrypted_content'] = decrypted_file_data  # Attach decrypted content to the file record

# #     else:
# #         evidence_list = []
    
# #     return render(request, 'evidence/evidence.html', {
# #         'court_case_number': court_case_number,  # Pass court_case_number to the template
# #         'evidence_list': evidence_list,  # Pass the evidence list to the template
# #     })

# def evidence_view(request):
#     # Get the court_case_number from GET request
#     court_case_number = request.GET.get('court_case_number', '')

#     # Get the case from the database using the court_case_number
#     case = get_case_by_number(court_case_number)
    
#     if case:
#         # If the case exists, find the evidence linked to this case
#         evidence_list = get_evidence_by_case_id(case['_id'])
        
#         # Decrypt sensitive fields for each evidence
#         for evidence in evidence_list:
#             # Decrypt text fields
#             if 'evidence_description' in evidence:
#                 evidence['evidence_description'] = decrypt_content(evidence['evidence_description'])
#             if 'remarks' in evidence:
#                 evidence['remarks'] = decrypt_content(evidence['remarks'])
            
#             # Decrypt files if necessary
#             if 'files' in evidence:
#                 for file in evidence['files']:
#                     # Fetch file from GridFS and decrypt the content
#                     file_id = file['file_id']
#                     file_data = fs.get(file_id).read()  # Retrieve file content from GridFS
#                     decrypted_file_data = decrypt_content(file_data)  # Decrypt the file data
#                     file['decrypted_content'] = decrypted_file_data  # Attach decrypted content to the file record

#     else:
#         evidence_list = []
    
#     return render(request, 'evidence/evidence.html', {
#         'court_case_number': court_case_number,  # Pass court_case_number to the template
#         'evidence_list': evidence_list,  # Pass the evidence list to the template
#     })


# def get_case_by_number(court_case_number):
#     case = cases_collection.find_one({'court_case_number': court_case_number})
#     return case

# def get_evidence_by_case_id(case_id):
#     evidence_list = list(evidence_collection.find({'case_id': case_id}))
#     return evidence_list

# import hashlib
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import padding
# from django.utils.crypto import get_random_string
# import base64

# # A helper function to ensure the SECRET_KEY is 256 bits (32 bytes)
# def get_valid_key(key):
#     return hashlib.sha256(key.encode()).digest()  # Hash to get a 32-byte key (256 bits)

# # Modify the encrypt_content function
# # def encrypt_content(content):
# #     # Ensure the key is 256 bits (32 bytes)
# #     key = get_valid_key('YourSecureKeyHere')  # Hash the key for AES

# #     # Create a random 16-byte IV for AES CBC mode
# #     iv = get_random_string(16).encode()
# #     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
# #     padder = padding.PKCS7(128).padder()
# #     padded_data = padder.update(content.encode()) + padder.finalize()
# #     encryptor = cipher.encryptor()
# #     encrypted_content = encryptor.update(padded_data) + encryptor.finalize()
# #     return base64.b64encode(iv + encrypted_content).decode()  # Store iv and encrypted content as base64

# # Modify the decrypt_content function
# # def decrypt_content(encrypted_content):
# #     # Ensure the key is 256 bits (32 bytes)
# #     key = get_valid_key('YourSecureKeyHere')  # Hash the key for AES
    
# #     # Decode the base64 content
# #     encrypted_content = base64.b64decode(encrypted_content)
# #     iv = encrypted_content[:16]  # Extract the IV
# #     encrypted_data = encrypted_content[16:]  # Extract the encrypted data

# #     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
# #     decryptor = cipher.decryptor()
# #     decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
# #     unpadder = padding.PKCS7(128).unpadder()
# #     decrypted_content = unpadder.update(decrypted_padded_data) + unpadder.finalize()
# #     return decrypted_content.decode()


# def encrypt_content(content):
#     key = get_valid_key('YourSecureKeyHere')  # Example key, should be stored securely
#     iv = os.urandom(16)  # Random IV for each encryption

#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     padder = padding.PKCS7(128).padder()
#     padded_data = padder.update(content.encode()) + padder.finalize()

#     encryptor = cipher.encryptor()
#     encrypted_content = encryptor.update(padded_data) + encryptor.finalize()

#     # Return IV + encrypted content as base64-encoded string
#     return base64.b64encode(iv + encrypted_content).decode()
# # Decrypt content using AES CBC mode
# import base64
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import padding
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# def decrypt_content(encrypted_content):
#     key = get_valid_key('YourSecureKeyHere')  # Securely retrieve the key

#     # Decode the base64 encoded content (if it was base64 encoded during encryption)
#     encrypted_content = base64.b64decode(encrypted_content)

#     # Extract the IV (the first 16 bytes) and the encrypted data (the rest)
#     iv = encrypted_content[:16]
#     encrypted_data = encrypted_content[16:]

#     # Initialize the AES cipher with CBC mode using the IV and key
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     decryptor = cipher.decryptor()

#     # Decrypt the data and get padded decrypted content
#     decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

#     # Unpad the decrypted content using PKCS7 unpadding
#     unpadder = padding.PKCS7(128).unpadder()
#     decrypted_content = unpadder.update(decrypted_padded_data) + unpadder.finalize()

#     # Decode the decrypted content to return as a string (assuming it was originally a UTF-8 string)
#     return decrypted_content.decode('utf-8')

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pymongo import MongoClient
from bson import ObjectId
import base64
import gridfs
import os
from datetime import datetime


fs = gridfs.GridFS(db)

# Encryption and Decryption functions
def get_cipher():
    key = settings.ENCRYPTION_KEY  # Already in bytes
    iv = settings.ENCRYPTION_IV  # Already in bytes
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    return cipher

def encrypt_content(plain_text):
    cipher = get_cipher()
    encryptor = cipher.encryptor()
    padded_data = plain_text + (16 - len(plain_text) % 16) * ' '
    encrypted_data = encryptor.update(padded_data.encode('utf-8')) + encryptor.finalize()
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_content(encrypted_text):
    cipher = get_cipher()
    decryptor = cipher.decryptor()
    encrypted_data = base64.b64decode(encrypted_text)
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data.decode('utf-8').rstrip()  # Remove padding

# from cryptography.hazmat.primitives import padding
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# import base64

# def decrypt_content(encrypted_text):
#     """Decrypts the content using the encryption key and IV from settings."""
#     # Decode the base64-encoded encrypted text
#     encrypted_data = base64.b64decode(encrypted_text)

#     # Get the cipher using the provided key and IV (settings should have these)
#     cipher = get_cipher()
#     decryptor = cipher.decryptor()

#     # Decrypt the data
#     decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

#     # Handle padding using PKCS7 and remove it
#     unpadder = padding.PKCS7(128).unpadder()  # AES block size is 128 bits (16 bytes)
#     unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

#     # Return the decrypted text as a string
#     return unpadded_data.decode('utf-8')

# Helper function to get case by court case number
def get_case_by_number(court_case_number):
    return cases_collection.find_one({'court_case_number': court_case_number})

# Helper function to get evidence by case ID
def get_evidence_by_case_id(case_id):
    return list(evidence_collection.find({'case_id': case_id}))

# Function to add evidence with encryption (WORKS)
# def add_evidence(request):
#     if request.method == 'POST':
#         court_case_number = request.POST.get('court_case_number')
#         case = get_case_by_number(court_case_number)
#         case_id = case.get('_id')
#         evidence_type = request.POST.get('evidence_type')
#         evidence_description = request.POST.get('evidence_description')
#         collected_by = request.POST.get('collected_by')
        
#         # Encrypt sensitive text fields
#         evidence_type_encrypted = encrypt_content(evidence_type)
#         evidence_description_encrypted = encrypt_content(evidence_description)
#         collected_by_encrypted = encrypt_content(collected_by)

#         # Handling file upload
#         uploaded_file = request.FILES.get('file')
#         file_data = uploaded_file.read()
#         file_name = uploaded_file.name
#         file_type = uploaded_file.content_type

#         # Save the file to GridFS
#         file_id = fs.put(file_data, filename=file_name, content_type=file_type)

#         # Create evidence document
#         evidence = {
#             "case_id": ObjectId(case_id),
#             "evidence_type": evidence_type_encrypted,
#             "evidence_description": evidence_description_encrypted,
#             "collected_by": collected_by_encrypted,
#             "files": [
#                 {
#                     "file_id": file_id,
#                     "file_type": file_type,
#                     "file_name": file_name,
#                     "file_size": len(file_data)
#                 }
#             ],
#             "upload_date": datetime.now()
#         }

#         # Insert evidence into the database
#         evidence_collection.insert_one(evidence)

#         # return HttpResponse("Evidence added successfully", status=200)
#     return render(request, 'evidence/add_evidence.html')

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def encrypt_file(file_data):
    # Encrypt the file content using the same key and IV from settings
    cipher = Cipher(algorithms.AES(settings.ENCRYPTION_KEY), modes.CBC(settings.ENCRYPTION_IV), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the file data
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(file_data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data

# def add_evidence(request):
#     if request.method == 'POST':
#         court_case_number = request.POST.get('court_case_number')
#         case = get_case_by_number(court_case_number)
#         case_id = case.get('_id')
#         evidence_type = request.POST.get('evidence_type')
#         evidence_description = request.POST.get('evidence_description')
#         collected_by = request.POST.get('collected_by')

#         # Encrypt sensitive text fields
#         evidence_type_encrypted = encrypt_content(evidence_type)
#         evidence_description_encrypted = encrypt_content(evidence_description)
#         collected_by_encrypted = encrypt_content(collected_by)

#         # Handling file upload
#         uploaded_file = request.FILES.get('file')
#         file_data = uploaded_file.read()
#         file_name = uploaded_file.name
#         file_type = uploaded_file.content_type

#         # Encrypt the file content
#         encrypted_file_data = encrypt_file(file_data)

#         # Save the encrypted file to GridFS
#         file_id = fs.put(encrypted_file_data, filename=file_name, content_type=file_type)

#         # Create evidence document
#         evidence = {
#             "case_id": ObjectId(case_id),
#             "evidence_type": evidence_type_encrypted,
#             "evidence_description": evidence_description_encrypted,
#             "collected_by": collected_by_encrypted,
#             "files": [
#                 {
#                     "file_id": file_id,
#                     "file_type": file_type,
#                     "file_name": file_name,
#                     "file_size": len(file_data)
#                 }
#             ],
#             "upload_date": datetime.now()
#         }

#         # Insert evidence into the database
#         evidence_collection.insert_one(evidence)

#     return render(request, 'evidence/add_evidence.html')

def add_evidence(request):
    if request.method == 'POST':
        court_case_number = request.POST.get('court_case_number')
        case = get_case_by_number(court_case_number)
        case_id = case.get('_id')
        evidence_type = request.POST.get('evidence_type')
        evidence_description = request.POST.get('evidence_description')
        collected_by = request.POST.get('collected_by')

        # Encrypt sensitive text fields
        evidence_type_encrypted = encrypt_content(evidence_type)
        evidence_description_encrypted = encrypt_content(evidence_description)
        collected_by_encrypted = encrypt_content(collected_by)

        # Handling file upload
        uploaded_file = request.FILES.get('file')
        file_data = uploaded_file.read()

        # Encrypt the file data
        encrypted_file_data = encrypt_file(file_data)
        file_name_encrypted = encrypt_content(uploaded_file.name)  # Encrypt file name
        file_type_encrypted = encrypt_content(uploaded_file.content_type)  # Encrypt file type
        file_size_encrypted = encrypt_content(str(len(file_data)))  # Encrypt file size (converted to string)

        # Save the encrypted file data to GridFS
        file_id = fs.put(encrypted_file_data, filename=uploaded_file.name, content_type=uploaded_file.content_type)

        # Create evidence document
        evidence = {
            "case_id": ObjectId(case_id),
            "evidence_type": evidence_type_encrypted,
            "evidence_description": evidence_description_encrypted,
            "collected_by": collected_by_encrypted,
            "files": [
                {
                    "file_id": file_id,
                    "file_name": file_name_encrypted,
                    "file_type": file_type_encrypted,
                    "file_size": file_size_encrypted,
                }
            ],
            "upload_date": datetime.now()
        }

        # Insert evidence into the database
        evidence_collection.insert_one(evidence)

    return render(request, 'evidence/add_evidence.html')


def evidence_view(request):
    # Get the court_case_number from GET request
    court_case_number = request.GET.get('court_case_number', '')

    # Get the case from the database using the court_case_number
    case = get_case_by_number(court_case_number)
    
    if case:
        # If the case exists, find the evidence linked to this case
        evidence_list = get_evidence_by_case_id(case['_id'])
        
        # Decrypt the necessary fields in each evidence item
        for evidence in evidence_list:
            if evidence.get('evidence_type'):
                evidence['evidence_type'] = decrypt_content(evidence['evidence_type'])
            if evidence.get('evidence_description'):
                evidence['evidence_description'] = decrypt_content(evidence['evidence_description'])
            if evidence.get('collected_by'):
                evidence['collected_by'] = decrypt_content(evidence['collected_by'])
        
    else:
        evidence_list = []

    return render(request, 'evidence/evidence.html', {
        'court_case_number': court_case_number,  # Pass court_case_number to the template
        'evidence_list': evidence_list,  # Pass the evidence list to the template
    })


def decrypt_file(encrypted_file_data):
    cipher = Cipher(algorithms.AES(settings.ENCRYPTION_KEY), modes.CBC(settings.ENCRYPTION_IV), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the file data
    decrypted_data = decryptor.update(encrypted_file_data) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data

# Function to view a file (decrypt and serve it)

def view_file(request, file_id):
    try:
        if isinstance(file_id, str):
            file_id = ObjectId(file_id)

        # Retrieve the file from GridFS
        file = fs.get(file_id)

        # Decrypt the file content
        decrypted_content = decrypt_file(file.read())

        # Serve the decrypted content based on content type
        response = HttpResponse(decrypted_content, content_type=file.content_type)

        if file.content_type.startswith('image'):
            response['Content-Type'] = file.content_type
        elif file.content_type == 'application/pdf':
            response['Content-Type'] = 'application/pdf'
        elif file.content_type == 'text/plain':
            response['Content-Type'] = 'text/plain'
        else:
            response['Content-Type'] = 'application/octet-stream'

        return response
    except gridfs.errors.NoFile:
        return HttpResponse("File not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error retrieving file: {str(e)}", status=500)

