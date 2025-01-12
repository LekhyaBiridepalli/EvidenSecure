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
                    "victim_names": [decrypt_content(name) for name in case.get("victim_names", [])],
                    "case_status": [decrypt_content(case["case_status"])]

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


