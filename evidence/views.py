from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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
    # You can pass any context data related to evidence here if needed
    return render(request, 'evidence/evidence.html')
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gridfs import GridFS
from bson.objectid import ObjectId
import datetime
from .db_utils import get_db
import json
from bson import ObjectId
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from .db_utils import get_db

@csrf_exempt
def upload_case(request):
    if request.method == 'POST':
        try:
            # Extract form data
            case_id = request.POST.get('case_id')
            case_type = request.POST.get('case_type')
            case_date = request.POST.get('case_date')
            accused_name = request.POST.get('accused_name')
            victim_name = request.POST.get('victim_name')
            investigating_officer = request.POST.get('investigating_officer')
            case_status = request.POST.get('case_status')
            court_case_number = request.POST.get('court_case_number')
            remarks = request.POST.get('remarks')

            # Validate required fields
            if not case_type:
                return JsonResponse({'error': 'case_type is required'}, status=400)
            if not investigating_officer:
                return JsonResponse({'error': 'investigating_officer is required'}, status=400)
            if not case_status:
                return JsonResponse({'error': 'case_status is required'}, status=400)
            if not case_id:
                return JsonResponse({'error': 'case_id is required'}, status=400)

            # Validate ObjectId format for case_id
            try:
                case_id = ObjectId(case_id)
            except Exception as e:
                return JsonResponse({'error': 'Invalid case_id format'}, status=400)

            # Validate case_date format
            if case_date:
                try:
                    case_date = datetime.datetime.strptime(case_date, '%Y-%m-%d')
                except ValueError:
                    return JsonResponse({'error': 'Invalid case_date format, expected YYYY-MM-DD'}, status=400)
            else:
                return JsonResponse({'error': 'case_date is required'}, status=400)

            # Connect to MongoDB and insert the case
            db = get_db()
            cases_collection = db['Cases']
            case_data = {
                "case_id": case_id,
                "case_type": case_type,
                "case_date": case_date,
                "accused_name": accused_name,
                "victim_name": victim_name,
                "investigating_officer": investigating_officer,
                "case_status": case_status,
                "court_case_number": court_case_number,
                "remarks": remarks
            }

            cases_collection.insert_one(case_data)
            return JsonResponse({'message': 'Case uploaded successfully!'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def upload_evidence(request):
    if request.method == 'POST':
        try:
            db = get_db()
            evidence_collection = db['Evidence']
            fs = GridFS(db)

            case_id = request.POST.get('case_id')
            evidence_type = request.POST.get('evidence_type')
            evidence_description = request.POST.get('evidence_description', '')
            collected_by = request.POST.get('collected_by', '')
            upload_date = request.POST.get('upload_date', str(datetime.datetime.now().date()))
            remarks = request.POST.get('remarks', '')

            files_data = []
            if request.FILES:
                for file in request.FILES.getlist('files'):
                    file_id = fs.put(file.read(), filename=file.name, content_type=file.content_type)
                    files_data.append({
                        "file_id": ObjectId(file_id),  # Ensure this is ObjectId
                        "file_type": file.content_type,
                        "file_name": file.name,
                        "file_size": file.size
                    })

            # Add evidence_id and other required fields
            evidence_data = {
                "evidence_id": ObjectId(),  # Unique ID for the evidence
                "case_id": ObjectId(case_id),
                "evidence_type": evidence_type,
                "evidence_description": evidence_description,
                "files": files_data,
                "collected_by": collected_by,
                "upload_date": datetime.datetime.strptime(upload_date, '%Y-%m-%d'),
                "remarks": remarks
            }

            evidence_collection.insert_one(evidence_data)
            return JsonResponse({'message': 'Evidence uploaded successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
