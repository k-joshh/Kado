from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from apps.reports.models import HazardReport, HazardTag

# Create your views here.
@login_required(login_url='login')
def home_view(request):
    past_24h = timezone.now() - timedelta(hours=24)
    recent_reports = (
        HazardReport.objects.filter(created_at__gte=past_24h)
        .prefetch_related('tags', 'images')
        .select_related('reporter')
        .order_by('-created_at')
    )

    all_reports = (
        HazardReport.objects.all()
        .prefetch_related('tags', 'images')
        .select_related('reporter')
        .order_by('-created_at')
    )

    tags = HazardTag.objects.all().order_by('name')

    reports_data = [
        {
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'status': r.status,
            'status_display': r.get_status_display(),
            'latitude': float(r.latitude),
            'longitude': float(r.longitude),
            'tracking_token': r.tracking_token,
            'photo_url': r.hazard_photo.url if r.hazard_photo else (r.images.first().image.url if r.images.all() else None),
            'tags': [t.name for t in r.tags.all()],
            'created_at': r.created_at.strftime('%b %d, %Y %I:%M %p'),
        }
        for r in all_reports
    ]

    return render(request, 'home/home.html', {
        'recent_reports': recent_reports,
        'reports_data': reports_data,
        'tags': tags,
    })
