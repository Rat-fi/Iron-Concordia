from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .forms import CustomUserCreationForm, EditProfileForm
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import CustomUser
from django.contrib.auth import update_session_auth_hash

# User Signup View
def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect('dashboard')  # Redirect to dashboard after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'User/signup.html', {'form': form})

# User Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('dashboard')  # Redirect to dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'User/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'User/dashboard.html')

# User Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

def send_verification_email(user):
    user.generate_verification_token()
    print(f"Generated Token: {user.verification_token}")  # Debugging

    verification_link = f"http://127.0.0.1:8000/user/verify/{user.verification_token}/"
    print(f"Verification Link: {verification_link}")  # Debugging

    send_mail(
        "Verify Your Email - CUFitness",
        f"Click the link to verify: {verification_link}",
        "ironconcordia.cufitness@gmail.com",
        [user.email],
        fail_silently=False,
    )

def verify_email(request, token=None):
    try:
        if not token:  # If no token is provided, generate a new one
            if request.user.is_authenticated:
                send_verification_email(request.user)
                messages.info(request, "A new verification email has been sent.")
                return redirect("dashboard")
            else:
                messages.error(request, "You must be logged in to verify your email.")
                return redirect("login")

        # Try to find a user with this token
        user = CustomUser.objects.get(verification_token=token)

        # Check if the token is expired
        if now() > user.verification_expires:
            messages.error(request, "This verification link has expired. Request a new one.")
            return redirect("dashboard")

        # Mark user as verified
        user.is_verified = True
        user.verification_token = None
        user.verification_expires = None
        user.save()

        messages.success(request, "Your email has been verified successfully!")
        return redirect("dashboard")

    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid verification link.")
        return redirect("dashboard")

@login_required
def delete_account(request):
    if request.method == "POST":
        password = request.POST.get("password")
        if check_password(password, request.user.password):
            request.user.delete()
            logout(request)
            return redirect("home")
    return render(request, "User/delete_account.html")

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # If a new password is entered, update it
            password = form.cleaned_data.get("password1")
            if password:
                user.set_password(password)

            user.save()

            # Ensure the user stays logged in after password change
            update_session_auth_hash(request, user)

            return redirect("dashboard")
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "User/edit_profile.html", {"form": form})