import json
import google.generativeai as genai
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm, LoginForm

# Configure Google Generative AI with the API key
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
                login(request, user)
                return redirect("dashboard")
    context = {'loginform': form}
    return render(request, 'WT/my-login.html', context=context)

# Logout view
def user_logout(request):
    logout(request)
    return redirect("/")

# Dashboard view (requires login)
@login_required(login_url="my-login")
def dashboard(request):
    return render(request, 'WT/dashboard.html')

# Hydration tracker view (requires login)
@login_required(login_url="my-login")
def hydration_tracker(request):
    return render(request, 'WT/hydration-tracker.html')

# Sleep tracker view (requires login)
@login_required(login_url="my-login")
def sleep_tracker(request):
    return render(request, 'WT/sleep-tracker.html')

# Chatbot view (requires login)
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
