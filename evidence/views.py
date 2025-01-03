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