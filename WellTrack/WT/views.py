from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .forms import CreateUserForm, LoginForm
from .models import SleepTracker, SleepLog  # Import SleepTracker and SleepLog models
import json
from transformers import pipeline
from datetime import date

# Set up the pipeline for text generation (using DistilGPT-2)
pipe = pipeline("text-generation", model="distilgpt2")

# In views.py, we already have the get_sleep_data method:
@login_required(login_url="my-login")
def get_sleep_data(request):
    tracker = SleepTracker.objects.filter(user=request.user).first()
    if tracker:
        sleep_goal = tracker.sleep_goal
    else:
        sleep_goal = 0  # Default if no goal is set

    logs = SleepLog.objects.filter(user=request.user).order_by('date')

    sleep_data = {
        "sleep_goal": sleep_goal,
        "logs": [{"date": log.date, "hours": log.hours} for log in logs]
    }
    return JsonResponse(sleep_data)

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

# Dashboard view (requires login)
@login_required(login_url="my-login")
def dashboard(request):
    return render(request, 'WT/dashboard.html')

# Chatbot view (Handles POST for responses and GET for page rendering)
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

# Hydration tracker view (requires login)
@login_required(login_url="my-login")
def hydration_tracker(request):
    return render(request, 'WT/hydration-tracker.html')

# Sleep tracker views (requires login)
@login_required(login_url="my-login")
def sleep_tracker(request):
    return render(request, 'WT/sleep-tracker.html')

# Endpoint to set sleep goal
@login_required(login_url="my-login")
def set_sleep_goal(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sleep_goal = data.get("sleep_goal")
        if sleep_goal and sleep_goal > 0:
            tracker, _ = SleepTracker.objects.get_or_create(user=request.user)
            tracker.sleep_goal = sleep_goal
            tracker.save()
            return JsonResponse({"message": "Sleep goal set successfully."})
        return JsonResponse({"error": "Invalid sleep goal."}, status=400)

# Endpoint to log sleep hours
@login_required(login_url="my-login")
def log_sleep(request):
    if request.method == "POST":
        try:
            # Parse the request body
            data = json.loads(request.body)
            log_date = data.get("date", str(date.today()))  # Default to today's date if no date is provided
            hours = data.get("hours")

            # Ensure 'hours' is provided and is a valid positive integer
            if hours is None:
                return JsonResponse({"error": "Sleep hours are required."}, status=400)

            try:
                # Convert 'hours' from string to integer, if necessary
                hours = int(hours)  # This will convert string to int if needed
                if hours <= 0:
                    return JsonResponse({"error": "Invalid sleep hours. Hours must be greater than 0."}, status=400)
            except ValueError:
                return JsonResponse({"error": "Invalid value for hours."}, status=400)

            # Proceed with saving the sleep log
            log, created = SleepLog.objects.get_or_create(user=request.user, date=log_date)
            log.hours = hours
            log.save()
            return JsonResponse({"message": "Sleep logged successfully."})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)

# Endpoint to retrieve sleep data
@login_required(login_url="my-login")
def get_sleep_data(request):
    tracker = SleepTracker.objects.filter(user=request.user).first()
    if tracker:
        sleep_goal = tracker.sleep_goal
    else:
        sleep_goal = 0  # Default if no goal is set

    logs = SleepLog.objects.filter(user=request.user).order_by('date')

    sleep_data = {
        "sleep_goal": sleep_goal,
        "logs": [{"date": log.date, "hours": log.hours} for log in logs]
    }
    return JsonResponse(sleep_data)
