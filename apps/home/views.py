from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from apps.reports.models import HazardReport

# Create your views here.
@login_required(login_url='login')
def home_view(request):
    past_24h = timezone.now() - timedelta(hours=24)
    recent_reports = (
        HazardReport.objects.filter(created_at__gte=past_24h)
        .select_related('category', 'reporter')
        .order_by('-created_at')
    )
    return render(request, 'home/home.html', {
        'recent_reports': recent_reports,
    })
