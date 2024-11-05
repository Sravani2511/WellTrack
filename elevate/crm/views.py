from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib import messages  # Add for success messages


# Homepage view
def homepage(request):
    return render(request, 'crm/index.html')


# Registration view
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')  # Display success message
            return redirect("my-login")  # Redirect to login page after registration

    context = {'registerform': form}
    return render(request, 'crm/register.html', context=context)


# Login view
def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")  # Add a welcome message
                return redirect("dashboard")  # Redirect to dashboard on successful login
            else:
                messages.error(request, 'Invalid username or password')  # Show error message for failed login

    context = {'loginform': form}
    return render(request, 'crm/my-login.html', context=context)


# Logout view
def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")  # Show a logout message
    return redirect("homepage")  # Redirect to homepage after logout


# Dashboard view (requires login)
@login_required(login_url="my-login")
def dashboard(request):
    return render(request, 'crm/dashboard.html')
