
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


import hashlib
import json
import logging
import base64
import os
from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.crypto import get_random_string

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from django.contrib.auth.hashers import make_password
import re


from pymongo import MongoClient
import gridfs
from bson import ObjectId

# Custom imports
from .db import *  
from .encryption import *

fs = gridfs.GridFS(db)

logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    return render(request, 'evidence/index.html')

import logging

# Set up logging
logger = logging.getLogger(__name__)


from bson import ObjectId

from django.contrib.auth.hashers import check_password
def login_view(request):
    if request.method == 'POST':
        # Get the email and password from the POST request
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Query MongoDB for the user
        user = users_collection.find_one({'email': email})

        if user and check_password(password, user['password']):

            request.session['user_id'] = str(user['_id'])
            return redirect('dashboard')
        else:
            # Handle invalid login
            return render(request, 'evidence/login.html', {'error': 'Invalid email or password'})

    return render(request, 'evidence/login.html')




# View for the signup page
def signup_view(request):
    if request.method == 'POST':
        # Extract data from the form
        name = request.POST.get('name')
        role = request.POST.get('role')
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact_number = request.POST.get('contact_number', None)
        department = request.POST.get('department')
        badge_number = request.POST.get('badge_number')

        # Validate required fields
        if not all([name, role, email, password, department, badge_number]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'evidence/signup.html', request.POST)

        # Email validation
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            messages.error(request, 'Invalid email address.')
            return render(request, 'evidence/signup.html', request.POST)

        # Check if the user already exists
        if users_collection.find_one({'email': email}):
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'evidence/signup.html', request.POST)

        # Hash the password
        hashed_password = make_password(password)

        # Create the user object
        user_data = {
            'name': name,
            'role': role,
            'email': email,
            'password': hashed_password,
            'contact_number': contact_number,
            'department': department,
            'badge_number': badge_number,
            'created_at': datetime.now()
        }

        # Insert the user into the MongoDB collection
        try:
            users_collection.insert_one(user_data)
            messages.success(request, 'Account created successfully. You can log in now!')
            return redirect('login')  # Redirect to login page
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'evidence/signup.html', request.POST)

    return render(request, 'evidence/signup.html')
# View for logging out the user
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the login page after logout


def dashboard(request):
    # Get the user_id from the session
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # Redirect if the user is not logged in

    try:
        # Convert user_id back to ObjectId to query MongoDB
        user_data = users_collection.find_one({'_id': ObjectId(user_id)})
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return redirect('login')
    
    total_cases = cases_collection.count_documents({})
    under_investigation_cases = cases_collection.count_documents({'case_status': encrypt_content('Under Investigation')})
    closed_cases = cases_collection.count_documents({'case_status': encrypt_content('Closed')})

    # Pass user_data to the template
    context = {
        'user_data': user_data,
        'total_cases': total_cases,
         'under_investigation_cases': under_investigation_cases,
         'closed_cases': closed_cases,
    }
    return render(request, 'evidence/dashboard.html', context)


def cases(request):
    # You can pass any context data related to cases here if needed
    return render(request, 'evidence/cases.html')

# Evidence Management View
def evidence(request):
    # You can pass any context data related to cases here if needed
    return render(request, 'evidence/evidence.html')






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

            # Encrypt fields
            encrypted_case_type = encrypt_content(case_type)
            encrypted_case_date = encrypt_content(case_date.strftime("%Y-%m-%d"))  # Encrypt as string
            encrypted_investigating_officer = encrypt_content(investigating_officer)
            encrypted_case_status = encrypt_content(case_status)
            encrypted_accused_names = [encrypt_content(name) for name in accused_names]
            encrypted_victim_names = [encrypt_content(name) for name in victim_names]
            encrypted_court_case_number = encrypt_content(court_case_number) if court_case_number else ''
            encrypted_remarks = encrypt_content(remarks) if remarks else ''
            encrypted_charges = [encrypt_content(charge) for charge in charges]

            # Generate a new case_id as ObjectId
            # case_id = ObjectId()  # This will create a valid ObjectId

            # Prepare the new case data
            new_case = {
                # "case_id": case_id,  # case_id should be ObjectId
                "case_type": encrypted_case_type,
                "case_registration_date": encrypted_case_date,
                "investigating_officer": encrypted_investigating_officer,
                "case_status": encrypted_case_status,
                "accused_names": encrypted_accused_names,  # Store as a list
                "victim_names": encrypted_victim_names,  # Store as a list
                "court_case_number": encrypted_court_case_number,
                "remarks": encrypted_remarks,
                "charges": encrypted_charges  # Store as a list
            }

            # Insert the encrypted case into MongoDB
            cases_collection.insert_one(new_case)

            # Redirect to the case list or show a success message
            return redirect('cases')  # Or return a success message as you see fit

        except Exception as e:
            # Handle any errors and send back a response
            return JsonResponse({"error": str(e)}, status=500)

    # If method is GET, render the add_case form
    return render(request, 'evidence/add_case.html')



def case_detail(request, case_id):
    try:
        # Fetch the case details using ObjectId
        case = cases_collection.find_one({"_id": ObjectId(case_id)})
        
        if not case:
            return HttpResponse("Case not found", status=404)

        # Decrypt the fields for display
        case_detail = {
            "id": str(case["_id"]),  # Convert ObjectId to string
            "case_type": decrypt_content(case["case_type"]),
            "case_registraion_date": decrypt_content(case["case_registration_date"]),  # Decrypt date as string
            "investigating_officer": decrypt_content(case["investigating_officer"]),
            "case_status": decrypt_content(case["case_status"]),
            "accused_names": [decrypt_content(name) for name in case.get("accused_names", [])],  # Decrypt list
            "victim_names": [decrypt_content(name) for name in case.get("victim_names", [])],  # Decrypt list
            "court_case_number": decrypt_content(case.get("court_case_number", "")),
            "remarks": decrypt_content(case.get("remarks", "")),
            "charges": [decrypt_content(charge) for charge in case.get("charges", [])]  # Decrypt list
        }

        # Render the case detail template
        return render(request, "evidence/case_detail.html", {"case": case_detail})

    except Exception as e:
        return HttpResponse(f"Error: {e}", status=400)


def cases(request):
    search_results = []

    try:
        # Get the search query from request
        query = request.GET.get('query', '')

        if query:
            # Perform a search with decrypted field comparisons
            # Fetch all cases from the database
            all_cases = cases_collection.find()
            
            # Decrypt all cases and filter them based on the query
            all_cases = [
                {
                    **case,
                    "case_id": str(case["_id"]),
                    "case_type": decrypt_content(case["case_type"]),
                    "court_case_number" : decrypt_content(case["court_case_number"]),
                    "accused_names": [decrypt_content(name) for name in case.get("accused_names", [])],
                    "victim_names": [decrypt_content(name) for name in case.get("victim_names", [])]
                }
                for case in all_cases
            ]

            # Filter decrypted cases based on the query
            search_results = [
                case for case in all_cases if
                query.lower() in case["case_type"].lower() or
                query in case["court_case_number"] or
                any(query.lower() in name.lower() for name in case["accused_names"]) or
                any(query.lower() in name.lower() for name in case["victim_names"])
            ]
        else:
            # If no query, fetch all cases and decrypt them
            all_cases = cases_collection.find()
            all_cases = [
                {
                    **case,
                    "case_id": str(case["_id"]),
                    "case_type": decrypt_content(case["case_type"]),
                    "court_case_number" : decrypt_content(case["court_case_number"]),
                    "accused_names": [decrypt_content(name) for name in case.get("accused_names", [])],
                    "victim_names": [decrypt_content(name) for name in case.get("victim_names", [])],
                    "case_status": [decrypt_content(case["case_status"])]
                }
                for case in all_cases
            ]

        # If no search query is provided, display all cases as search results
        search_results = search_results or all_cases

        # Render the cases list with all cases and search results
        return render(request, 'evidence/cases.html', {'all_cases': all_cases, 'search_results': search_results})

    except Exception as e:
        # Handle any errors and log them
        return HttpResponse(f"Error: {e}", status=500)




def get_case_by_number(court_case_number):
    return cases_collection.find_one({'court_case_number': encrypt_content(court_case_number)})

# Helper function to get evidence by case ID
def get_evidence_by_case_id(case_id):
    return list(evidence_collection.find({'case_id': case_id}))



def add_evidence(request):
    if request.method == 'POST':
        court_case_number = request.POST.get('court_case_number')
        case = get_case_by_number(court_case_number)

        # Check if case exists
        if not case:
            return redirect('add_evidence')  # Redirect back to the form

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
        try:
            evidence_collection.insert_one(evidence)
            messages.success(request, 'Evidence added successfully.')
            return redirect('evidence')  # Redirect to the evidence management page or success page
        except Exception as e:
            logger.error(f"Error inserting evidence into database: {str(e)}")
            return HttpResponse(f"Error inserting evidence into database: {str(e)}", status=500)

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


