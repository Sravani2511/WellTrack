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
import google.generativeai as genai
from django.contrib.auth import authenticate, login, logout

genai.configure(api_key="AIzaSyAxKriskOxxJ4L9O4qKwmGxHDPiIlaP5X8")

# Define generation configuration (defined once, outside of the request handler)
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create a model with the system instruction (also defined once)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "You are a virtual healthcare assistant designed to provide empathetic, "
        "evidence-based guidance on general health concerns and wellness tips. "
        "Maintain a warm, supportive, and professional tone, avoiding medical jargon "
        "unless necessary. Offer concise, user-friendly suggestions while emphasizing "
        "that users consult healthcare providers for serious or specific issues. Avoid "
        "diagnosing or prescribing treatments; instead, guide users with general advice "
        "and encourage follow-ups (e.g., 'Let me know if there's anything else I can help with.'). "
        "In emergencies (e.g., 'I have chest pain.'), immediately advise contacting emergency services. "
        "Prioritize safety, clarity, and support in every response."
    ),
)


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
    if request.method == 'POST':
        # Parse incoming JSON data
        try:
            data = json.loads(request.body)
            user_input = data.get('user_input', '')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if not user_input:
            return JsonResponse({'error': 'No user input provided'}, status=400)

        # Initialize the chatbot session
        chat_session = model.start_chat(history=[])

        try:
            # Send the user's message and get the response from the model
            response = chat_session.send_message(user_input)

            if response and hasattr(response, 'text'):
                bot_response = response.text.strip()
            else:
                bot_response = "Sorry, I couldn't get a valid response from the system."
        except Exception as e:
            bot_response = f"An error occurred: {str(e)}"

        # Log the response for debugging purposes
        print(f"Bot response: {bot_response}")

        # Return the bot's response as JSON
        return JsonResponse({'bot_response': bot_response})

    # If the request is not a POST, render the chatbot template
    return render(request, 'WT/chatbot.html')

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
def confirm_appointment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        appointment_date = request.POST.get("appointment_date")
        description = request.POST.get("description")

        # Save the appointment to the database
        Appointment.objects.create(
            name=name,
            appointment_date=appointment_date,
            description=description
        )
        return redirect("appointments-list")  # Redirect to the appointments list

    return render(request, "book_appointment.html")

def modify_appointment(request, appointment_id=None):
    # Check if there are any appointments in the database
    if not Appointment.objects.exists():
        messages.warning(request, "No appointments available to modify.")
        return redirect("appointments-list")  # Redirect to the appointments list

    # Get the specific appointment for modification
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "POST":
        # Update the appointment details if POST request
        appointment.name = request.POST.get("name")
        appointment.appointment_date = request.POST.get("appointment_date")
        appointment.description = request.POST.get("description")
        appointment.save()
        messages.success(request, "Appointment updated successfully!")
        return redirect("appointments-list")  # Redirect to the appointments list

    return render(request, "modify_appointment.html", {"appointment": appointment})

def delete_appointment(request):
    if request.method == "POST":
        name = request.POST.get("name").strip()
        
        # Check if an appointment with the given name exists
        appointment = Appointment.objects.filter(name=name).first()

        if not appointment:
            # No matching appointment found
            messages.error(request, "No appointment found with the given name.")
            return render(request, "delete_appointment.html")

        # Delete the matching appointment
        appointment.delete()
        messages.success(request, f"Appointment '{name}' has been successfully deleted.")
        return redirect("appointments-list")

    return render(request, "delete_appointment.html")
