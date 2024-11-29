from django.contrib.auth.models import User  # Import the User model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout, authenticate
from .forms import  LoginForm,RegisterForm

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()  # Display the empty registration form
        return render(request, 'users/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)  # Get form data from the POST request
        
        if form.is_valid():  # Validate the form data
            username = form.cleaned_data.get('username').lower()
            
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists. Please choose a different one.')
                return render(request, 'users/register.html', {'form': form})

            # Create user if username is unique
            user = form.save(commit=False)
            user.username = username  # Ensure the username is lowercase
            user.save()  # Save the user object to the database

            # Set the flash success message
            messages.success(request, 'You have signed up successfully.')
            
            # Log the user in and redirect to the posts page
            login(request, user)
            return redirect('posts')

        else:
            # If form is invalid, re-render the form with error messages
            return render(request, 'users/register.html', {'form': form})

def sign_in(request):
    """
    Handle the login process.
    If the user is already authenticated, redirect to the posts page.
    If not, authenticate and log the user in upon valid credentials.
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('posts')  # Redirect to posts if already logged in
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('posts')  # Redirect to posts page after successful login
        messages.error(request, 'Invalid username or password')
        return render(request, 'users/login.html', {'form': form})

def sign_out(request):
    """
    Log out the user and redirect to the login page.
    """
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')  # Redirect to the login page after logout


