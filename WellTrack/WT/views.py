from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .forms import CreateUserForm, LoginForm
from .models import CalorieLog  # Import the CalorieLog model
import json
from transformers import pipeline
from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment
from WT.models import Appointment


# Set up the pipeline for text generation (using DistilGPT-2)
pipe = pipeline("text-generation", model="distilgpt2")

# Home page view
def homepage(request):
    return render(request, 'WT/index.html')

# Registration view
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my-login")
    context = {'registerform': form}
    return render(request, 'WT/register.html', context=context)

# Login view
def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    context = {'loginform': form}
    return render(request, 'WT/my-login.html', context=context)

# Logout view
def user_logout(request):
    auth.logout(request)
    return redirect("homepage")

# Chatbot view
@login_required(login_url="my-login")
def chatbot(request):
    chat_history = request.session.get("chat_history", [])
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("user_message")
            if not user_message:
                return JsonResponse({"error": "No user message provided"}, status=400)
            chat_history.append({"user": True, "text": user_message})
            bot_response = pipe(user_message, max_length=100)[0]['generated_text'].strip()
            chat_history.append({"user": False, "text": bot_response})
            if len(chat_history) > 20:
                chat_history = chat_history[-20:]
            request.session["chat_history"] = chat_history
            return JsonResponse({"message": bot_response})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    request.session["chat_history"] = []
    return render(request, "WT/chatbot.html", {"chat_history": []})

# Dashboard view (requires login)
@login_required(login_url="my-login")
def dashboard(request):
    return render(request, 'WT/dashboard.html')

# Hydration tracker view
@login_required(login_url="my-login")
def hydration_tracker(request):
    return render(request, 'WT/hydration-tracker.html')

# Sleep tracker view
@login_required(login_url="my-login")
def sleep_tracker(request):
    return render(request, 'WT/sleep-tracker.html')

# Calorie tracker view
@login_required(login_url="my-login")
def calorie_tracker(request):
    return render(request, 'WT/calorie-tracker.html')

# Appointment Manager view
@login_required(login_url="my-login")
def appointment_manager(request):
    # Implement your logic for the appointment manager here
    # For now, render a placeholder HTML page
    return render(request, 'WT/appointment-manager.html')

def add_appointment(request):
    if request.method == 'POST':
        # Extract data from form submission
        name = request.POST.get('name')
        appointment_date = request.POST.get('appointment_date')
        description = request.POST.get('description')
        
        # Save the appointment (you should handle form validation here)
        Appointment.objects.create(
            name=name,
            appointment_date=appointment_date,
            description=description
        )
        
        # Redirect or render a success message
        return redirect('appointment-success')  # Adjust redirect as necessary
    
    return render(request, 'add-appointment.html')

def add_reminder(request):
    return render(request, 'WT/add_reminder.html')


def book_appointment(request, appointment_id):
    # Retrieve the appointment by ID
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        # Confirm the appointment (e.g., update a 'status' field in your model)
        appointment.status = 'Confirmed'  # Assuming you have a 'status' field
        appointment.save()
        
        return redirect('appointment-confirmed')  # Redirect to a confirmation page
    
    return render(request, 'book_appointment.html', {'appointment': appointment})

