from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.login.models import User

@login_required(login_url='login')
def setup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        barangay = request.POST.get('barangay', '').strip()

        if first_name == '' or last_name == '' or phone_number == '' or barangay == '':
            messages.error(request, "Please fill out all fields.")
        else:
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.phone_number = phone_number
            request.user.barangay = barangay

            request.user.save()
            return redirect('home')

    return render(request, 'setup/setup.html', {
        'barangay_choices': User.BARANGAY_CHOICES,
    })
