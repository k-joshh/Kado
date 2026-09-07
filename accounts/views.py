from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages


# Create your views here.
User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        conf_password = request.POST.get('conf_password', '')

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
        elif password != conf_password:
            messages.error(request, "Passwords do not match.")
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            return redirect('login')

    return render(request, 'accounts/register.html')

def home_view(request):
    return render(request, 'accounts/home.html')