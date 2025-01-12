from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .db import *  # Import the MongoDB connection


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

# def cases(request):
#     query = request.GET.get('query', '')  # Get search query from URL parameters
#     if query:
#         # Search for cases by case_id or title
#         search_results = cases_collection.find({
#             '$or': [
#                 {'case_id': {'$regex': query, '$options': 'i'}},
#                 {'title': {'$regex': query, '$options': 'i'}}
#             ]
#         })
#     else:
#         search_results = []

#     # Fetch all cases for the "All Cases" section
#     all_cases = cases_collection.find()

#     # Convert MongoDB cursors to lists
#     search_results = list(search_results)
#     all_cases = list(all_cases)

#     return render(request, 'evidence/cases.html', {
#         'search_results': search_results,
#         'all_cases': all_cases
#     })


# # View to Add Case
# def add_case(request):
#     if request.method == 'POST':
#         case_data = {
#             "case_id": request.POST.get('case_id'),
#             "title": request.POST.get('title'),
#             "description": request.POST.get('description'),
#             "officer_id": request.POST.get('officer_id'),
#             "status": request.POST.get('status'),
#         }
#         cases_collection.insert_one(case_data)  # Save case in MongoDB
#         return redirect('cases')  # Redirect to cases page
#     return render(request, 'evidence/addcase.html')  # Render Add Case page

# def case_detail(request, case_id):
#     # Fetch the case details from MongoDB
#     case = cases_collection.find_one({'case_id': case_id})
#     if not case:
#         return render(request, '404.html', status=404)  # Handle case not found

#     return render(request, 'evidence/case_detail.html', {'case': case})

# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# from .db import cases_collection
# from bson.objectid import ObjectId
# from django.http import JsonResponse
# from django.shortcuts import render
# from pymongo import MongoClient

# # # Set up MongoDB client
# # client = MongoClient('mongodb://localhost:27017/')  # Make sure the MongoDB URI is correct
# # db = client['EvidenSecure_db']  # Name of your database
# # cases_collection = db['Cases']  # Your collection name

# # def cases(request):
# #     search_results = []
    
# #     # Check if there's a search query
# #     query = request.GET.get('query', '')
# #     if query:
# #         search_results = list(cases_collection.find({
# #             "$or": [
# #                 {"case_type": {"$regex": query, "$options": "i"}},  # Case type search
# #                 {"accused_name": {"$regex": query, "$options": "i"}},  # Accused name search
# #                 {"victim_name": {"$regex": query, "$options": "i"}}  # Victim name search
# #             ]
# #         }))
# #     else:
# #         search_results = list(cases_collection.find())  # Fetch all cases if no search query
    
# #     context = {
# #         'search_results': search_results
# #     }
    
# #     return render(request, 'evidence/cases.html', context)


# # def case_detail(request, case_id):
# #     # Fetch the case details using ObjectId
# #     case = cases_collection.find_one({"_id": ObjectId(case_id)})
# #     if not case:
# #         return HttpResponse("Case not found", status=404)
    
# #     case["id"] = str(case["_id"])
# #     return render(request, "evidence/case_detail.html", {"case": case})

# from bson import ObjectId
# from django.shortcuts import render
# from django.http import HttpResponse
# from datetime import datetime

# # def cases(request):
# #     query = request.GET.get("query", "")  # Search query from the form (if any)

# #     # Fetch search results if a query is provided
# #     search_results = []
# #     if query:
# #         search_results = list(
# #             cases_collection.find({
# #                 "$or": [
# #                     {"case_type": {"$regex": query, "$options": "i"}},
# #                     {"accused_name": {"$regex": query, "$options": "i"}},
# #                     {"victim_name": {"$regex": query, "$options": "i"}}
# #                 ]
# #             })
# #         )
# #         # Convert ObjectId to string for the template
# #         for case in search_results:
# #             case["id"] = str(case["_id"])
# #     else:
# #         # If no search query, get all cases
# #         search_results = list(cases_collection.find())

# #     # Fetch all cases for the "All Cases List" section (sorted by case date)
# #     all_cases = list(cases_collection.find().sort("case_date", -1))
# #     for case in all_cases:
# #         case["id"] = str(case["_id"])  # Convert ObjectId to string for template

# #     context = {
# #         "search_results": search_results,
# #         "all_cases": all_cases
# #     }
    
# #     return render(request, "evidence/cases.html", context)

# def cases(request):
#     search_results = []
    
#     # If there is a query in the search input
#     query = request.GET.get('query', '')
    
#     # If the search query exists, filter cases based on the query
#     if query:
#         search_results = cases_collection.find({
#             "$or": [
#                 {"case_type": {"$regex": query, "$options": "i"}},  # Search in case_type
#                 {"accused_name": {"$regex": query, "$options": "i"}},  # Search in accused_name
#                 {"victim_name": {"$regex": query, "$options": "i"}}  # Search in victim_name
#             ]
#         })
#     else:
#         # Fetch all cases if no search query is provided
#         search_results = cases_collection.find()

#     all_cases = cases_collection.find()
#     all_cases = [{**case, "case_id": str(case["_id"])} for case in all_cases]
#     search_results = [{**case, "case_id": str(case["_id"])} for case in search_results]


#     return render(request, 'evidence/cases.html', { 'all_cases': all_cases,'search_results': search_results, })

# # def case_detail(request, case_id):
# #     # Fetch the case details using ObjectId
# #     case = cases_collection.find_one({"_id": ObjectId(case_id)})
# #     if not case:
# #         return HttpResponse("Case not found", status=404)
    
# #     case["id"] = str(case["_id"])  # Convert ObjectId to string for template
# #     return render(request, "evidence/case_detail.html", {"case": case})

# def case_detail(request, case_id):
#     # Fetch the case details using ObjectId
#     try:
#         case = cases_collection.find_one({"_id": ObjectId(case_id)})
#     except Exception as e:
#         return HttpResponse(f"Error: {e}", status=400)
    
#     if not case:
#         return HttpResponse("Case not found", status=404)

#     # Convert ObjectId to string for display
#     case["id"] = str(case["_id"])
#     case["case_date"] = case["case_date"].strftime('%Y-%m-%d')  # Format the date as string

#     return render(request, "evidence/case_detail.html", {"case": case})

# # def add_case(request):
# #     if request.method == "POST":
# #         case_data = {
# #             "case_type": request.POST.get("case_type"),
# #             "case_date": request.POST.get("case_date"),
# #             "accused_name": request.POST.get("accused_name"),
# #             "victim_name": request.POST.get("victim_name"),
# #             "investigating_officer": request.POST.get("investigating_officer"),
# #             "case_status": request.POST.get("case_status"),
# #             "court_case_number": request.POST.get("court_case_number"),
# #             "remarks": request.POST.get("remarks"),
# #         }
# #         cases_collection.insert_one(case_data)
# #         return render(request, "evidence/cases.html")
    
# #     return render(request, "evidence/add_case.html")

# # def add_case(request):
# #     if request.method == 'POST':
# #         # Get data from the request body (assuming the data is sent as form data or JSON)
# #         case_data = request.POST
        
# #         # Create a new case dictionary that matches your schema
# #         new_case = {
# #             'case_id': case_data.get('case_id'),  # Assuming this is a unique identifier
# #             'case_type': case_data.get('case_type'),  # Type of case, e.g., Murder
# #             'case_date': datetime.strptime(case_data.get('case_date'), "%Y-%m-%d"),  # Parse date string
# #             'accused_name': case_data.get('accused_name'),
# #             'victim_name': case_data.get('victim_name'),
# #             'investigating_officer': case_data.get('investigating_officer'),
# #             'case_status': case_data.get('case_status'),
# #             'court_case_number': case_data.get('court_case_number'),
# #             'remarks': case_data.get('remarks')
# #         }

# #         # Insert the new case into the database
# #         result = cases_collection.insert_one(new_case)

# #         # Return a success response with the case ID
# #         if result.inserted_id:
# #             return JsonResponse({'message': 'Case added successfully!', 'case_id': str(result.inserted_id)}, status=201)
# #         else:
# #             return JsonResponse({'message': 'Failed to add case.'}, status=500)

# #     # If it's not a POST request, render the case addition page
# #     return render(request, 'evidence/add_case.html')

# # In your views.py
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from datetime import datetime
# import json
# from bson import ObjectId
# from datetime import datetime
# import json

# # @csrf_exempt
# # def add_case(request):
# #     if request.method == 'POST':
# #         try:
# #             # Log the raw request body for debugging
# #             print("Raw Request Body:", request.body)

# #             case_data = json.loads(request.body)

# #             # Convert case_id to ObjectId if needed
# #             case_id = ObjectId()  # Automatically generates a unique ObjectId if case_id is not provided
# #             if 'case_id' in case_data:
# #                 case_id = ObjectId(case_data.get('case_id'))  # If you are sending case_id as a string, convert it to ObjectId

# #             # Parse the case_date if it's present
# #             case_date = datetime.strptime(case_data.get('case_date'), "%Y-%m-%d") if 'case_date' in case_data else None

# #             # Create the new case dictionary to insert into MongoDB
# #             new_case = {
# #                 "case_id": case_id,
# #                 "case_type": case_data.get('case_type'),
# #                 "case_date": case_date,
# #                 "investigating_officer": case_data.get('investigating_officer'),
# #                 "case_status": case_data.get('case_status'),
# #                 "accused_name": case_data.get('accused_name', ''),
# #                 "victim_name": case_data.get('victim_name', ''),
# #                 "court_case_number": case_data.get('court_case_number', ''),
# #                 "remarks": case_data.get('remarks', '')
# #             }

# #             # Insert the case into the MongoDB collection
# #             result = cases_collection.insert_one(new_case)  # Insert into MongoDB

# #             return JsonResponse({"message": "Case added successfully!", "case_id": str(result.inserted_id)}, status=201)

# #         except json.JSONDecodeError as e:
# #             return JsonResponse({"error": f"Invalid JSON data: {str(e)}"}, status=400)
# #         except Exception as e:
# #             return JsonResponse({"error": str(e)}, status=500)

# #     return JsonResponse({"error": "Only POST method allowed"}, status=405)

# from bson import ObjectId
# from datetime import datetime
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# import json
# def add_case(request):
#     if request.method == 'POST':
#         try:
#             # Capture form data
#             case_type = request.POST.get('case_type')
#             case_date = request.POST.get('case_date')
#             investigating_officer = request.POST.get('investigating_officer')
#             case_status = request.POST.get('case_status')
#             accused_name = request.POST.get('accused_name', '')
#             victim_name = request.POST.get('victim_name', '')
#             court_case_number = request.POST.get('court_case_number', '')
#             remarks = request.POST.get('remarks', '')

#             # Validate required fields
#             if not case_type or not case_date or not investigating_officer or not case_status:
#                 return JsonResponse({"error": "Missing required fields: case_type, case_date, investigating_officer, case_status"}, status=400)

#             # Convert case_date to datetime
#             try:
#                 case_date = datetime.strptime(case_date, "%Y-%m-%d")
#             except ValueError:
#                 return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

#             # Generate a new case_id as ObjectId
#             case_id = ObjectId()  # This will create a valid ObjectId

#             # Prepare the new case data
#             new_case = {
#                 "case_id": case_id,  # case_id should be ObjectId
#                 "case_type": case_type,
#                 "case_date": case_date,
#                 "investigating_officer": investigating_officer,
#                 "case_status": case_status,
#                 "accused_name": accused_name,
#                 "victim_name": victim_name,
#                 "court_case_number": court_case_number,
#                 "remarks": remarks
#             }

#             # Insert the case into MongoDB
#             result = cases_collection.insert_one(new_case)

#             # Redirect to the case list or show a success message
#             return redirect('cases')  # Or return a success message as you see fit

#         except Exception as e:
#             # Handle any errors and send back a response
#             return JsonResponse({"error": str(e)}, status=500)

#     # If method is GET, render the add_case form
#     return render(request, 'evidence/add_case.html')

from bson import ObjectId
from datetime import datetime
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


# def get_case_evidence(request, case_id):
#     # Fetch evidence for the case from MongoDB
#     evidence_list = evidence_collection.find({"case_id": ObjectId(case_id)})

#     # Convert MongoDB documents to JSON-friendly format
#     evidence_data = [{
#         'evidence_id': str(evidence['_id']),
#         'evidence_type': evidence['evidence_type'],
#         'collected_by': evidence['collected_by'],
#         'upload_date': evidence['upload_date']
#     } for evidence in evidence_list]

#     return JsonResponse({'evidences': evidence_data})


# def add_evidence(request):
#     case_id = request.GET.get('case_id')
    
#     if request.method == 'POST':
#         # Process the form data to insert evidence into the MongoDB database
#         evidence_type = request.POST.get('evidence_type')
#         evidence_description = request.POST.get('evidence_description')
#         evidence_file = request.FILES.get('evidence_file')

#         # For simplicity, let's assume evidence is stored in the filesystem and the path is saved
#         # If you're saving to GridFS or another system, adjust accordingly
#         evidence_file_path = 'path_to_file'  # Save or store the file path

#         evidence_data = {
#             'case_id': ObjectId(case_id),  # Link evidence to case by ID
#             'evidence_type': evidence_type,
#             'evidence_description': evidence_description,
#             'evidence_file': evidence_file_path,
#             'upload_date': '2025-01-05',  # Use current date or datetime
#             'collected_by': 'Inspector Name'  # You can retrieve this dynamically
#         }

#         # Insert evidence into MongoDB collection
#         evidence_collection.insert_one(evidence_data)

#         return redirect(f'/evidence/?case_id={case_id}')

#     # If GET request, show the form for adding evidence
#     return render(request, 'add_evidence.html', {'case_id': case_id})

from django.shortcuts import render, redirect
from django.conf import settings
from pymongo import MongoClient
from bson import ObjectId
import gridfs
import os

from django.core.files.uploadedfile import InMemoryUploadedFile





# Evidence View (Search evidence by case number and display it)
# def evidence_view(request):
#     case_number = request.GET.get('case_number', '')  # Case number from user input
#     evidence_list = []
#     error_message = ""

#     if case_number:
#         case = cases_collection.find_one({"case_number": case_number})  # Search case by case number
#         if case:
#             case_id = case['_id']
#             evidence_list = list(evidence_collection.find({"case_id": ObjectId(case_id)}))

#             # Add file URLs for GridFS files
#             for evidence in evidence_list:
#                 if 'files' in evidence and len(evidence['files']) > 0:
#                     file_id = evidence['files'][0]['file_id']
#                     file_data = fs.get(file_id)
#                     evidence['file_url'] = f"/media/{file_id}"
#         else:
#             error_message = f"Case with number {case_number} not found."

#     return render(request, 'evidence/evidence.html', {
#         'case_number': case_number,
#         'evidence_list': evidence_list,
#         'error_message': error_message
#     })
# views.py


def evidence_view(request):
    # Get the court_case_number from GET request
    court_case_number = request.GET.get('court_case_number', '')

    # Get the case from the database using the court_case_number
    case = get_case_by_number(court_case_number)
    
    if case:
        # If the case exists, find the evidence linked to this case
        evidence_list = get_evidence_by_case_id(case['_id'])
    else:
        evidence_list = []
    
    return render(request, 'evidence/evidence.html', {
        'court_case_number': court_case_number,  # Pass court_case_number to the template
        'evidence_list': evidence_list,  # Pass the evidence list to the template
    })

# # Add Evidence View (Insert new evidence into MongoDB)
# def add_evidence_view(request):
#     if request.method == 'POST':
#         # Collect case number and verify it
#         case_number = request.POST['case_number']
#         case = cases_collection.find_one({"case_number": case_number})

#         if not case:
#             return render(request, 'evidence/add_evidence.html', {
#                 'error_message': f"Case with number {case_number} not found.",
#                 'case_number': case_number
#             })

#         # Case ID and evidence data preparation
#         case_id = case['_id']
#         evidence_data = {
#             "case_id": ObjectId(case_id),
#             "evidence_type": request.POST['evidence_type'],
#             "evidence_description": request.POST['evidence_description'],
#             "collected_by": request.POST['collected_by'],
#             "upload_date": request.POST['upload_date'],
#             "remarks": request.POST.get('remarks', ''),
#         }

#         # Handle file upload
#         if 'file' in request.FILES:
#             file = request.FILES['file']
#             file_id = fs.put(file, filename=file.name, content_type=file.content_type)
#             evidence_data['files'] = [{
#                 "file_id": file_id,
#                 "file_type": file.content_type,
#                 "file_name": file.name,
#             }]

#         # Insert evidence into MongoDB
#         evidence_collection.insert_one(evidence_data)
#         return redirect('evidence')  # Redirect to the evidence page after adding evidence

#     # Display Add Evidence form
#     case_number = request.GET.get('case_number', '')
#     return render(request, 'evidence/add_evidence.html', {'case_number': case_number})

from django.core.files.storage import FileSystemStorage
from django.utils import timezone


from django.shortcuts import render, redirect
from django.http import HttpResponse
from pymongo import MongoClient
import gridfs
from django.utils import timezone

fs = gridfs.GridFS(db)

def add_evidence(request):
    if request.method == 'POST':
        # Get the case number input from the form
        court_case_number = request.POST.get('court_case_number')

        # Retrieve the case object by case number
        case = get_case_by_number(court_case_number)
        
        if case:
            # Extract case_id from the case object
            case_id = case.get('_id')  # or 'id' depending on your MongoDB setup

            # Now extract other form data
            evidence_type = request.POST.get('evidence_type')
            evidence_description = request.POST.get('evidence_description')
            collected_by = request.POST.get('collected_by')
            remarks = request.POST.get('remarks', '')  # Optional field
            upload_date = timezone.now()  # Use current timestamp for upload date

            # Handle file upload
            uploaded_file = request.FILES.get('file')  # Handle file upload from form
            if uploaded_file:
                # Save the file to GridFS
                file_id = fs.put(uploaded_file.read(), filename=uploaded_file.name)
                file_type = uploaded_file.content_type  # Extract file type (e.g., image/jpeg)
                file_name = uploaded_file.name  # Original file name
                file_size = uploaded_file.size  # File size in bytes

                # Construct the files array as required by the schema
                files = [{
                    'file_id': file_id,
                    'file_type': file_type,
                    'file_name': file_name,
                    'file_size': file_size
                }]
            else:
                # Handle the case where file is not uploaded (you could set an empty array or handle error)
                files = []

            # Create the evidence document to be inserted into MongoDB
            new_evidence = {
                'case_id': case_id,
                'evidence_type': evidence_type,
                'evidence_description': evidence_description,
                'collected_by': collected_by,
                'upload_date': upload_date,
                'remarks': remarks,
                'files': files  # Reference to files in GridFS
            }

            # Insert the document into the evidence collection
            try:
                evidence_collection.insert_one(new_evidence)
                return redirect('evidence')  # Redirect to the evidence management page or success page
            except Exception as e:
                return HttpResponse(f"Error inserting evidence: {str(e)}", status=500)

        else:
            # Case not found
            return HttpResponse("Case not found", status=404)

    return render(request, 'evidence/add_evidence.html')


def save_file_to_gridfs(file: InMemoryUploadedFile):
    """
    This function takes an uploaded file (InMemoryUploadedFile or File object),
    stores it in GridFS, and returns the GridFS file ID.
    """
    # Store the file in GridFS
    file_id = fs.put(file, filename=file.name, content_type=file.content_type)
    return file_id

def get_file_from_gridfs(file_id):
    file = fs.get(file_id)  # Retrieve file from GridFS using file_id
    return file
