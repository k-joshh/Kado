from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

User = get_user_model()

# Create your views here.
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

    return render(request, 'register/register.html')