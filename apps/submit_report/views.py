import uuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse
from apps.reports.models import HazardReport, HazardReportImage, HazardTag


def generate_unique_token():
    while True:
        token_suffix = uuid.uuid4().hex[:8].upper()
        token = f"RPT-{token_suffix[:4]}-{token_suffix[4:]}"
        if not HazardReport.objects.filter(tracking_token=token).exists():
            return token


@login_required(login_url='login')
def submit_report_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        tags_raw = request.POST.get('tags', '').strip()
        location_name = request.POST.get('location_name', '').strip()
        latitude_str = request.POST.get('latitude', '').strip()
        longitude_str = request.POST.get('longitude', '').strip()
        description = request.POST.get('description', '').strip()
        images = request.FILES.getlist('images')

        errors = []
        if not title:
            errors.append("Report Title is required.")
        if not tags_raw:
            errors.append("At least one tag is required.")
        if not location_name or not latitude_str or not longitude_str:
            errors.append("Location is required. Please select a location on the map.")
        if not description:
            errors.append("Description is required.")
        if not images:
            errors.append("At least one image must be uploaded or taken with camera.")

        try:
            latitude = float(latitude_str)
            longitude = float(longitude_str)
        except (ValueError, TypeError):
            errors.append("Invalid coordinates provided.")
            latitude = None
            longitude = None

        if errors:
            all_tags = HazardTag.objects.all().order_by('name')
            return render(request, 'submit_report/submit_report.html', {
                'tags': all_tags,
                'errors': errors,
                'form_data': {
                    'title': title,
                    'tags': tags_raw,
                    'location_name': location_name,
                    'latitude': latitude_str,
                    'longitude': longitude_str,
                    'description': description,
                }
            }, status=400)

        # Generate unique tracking token
        tracking_token = generate_unique_token()

        # Primary photo
        primary_photo = images[0] if images else None

        # Create HazardReport
        report = HazardReport.objects.create(
            tracking_token=tracking_token,
            reporter=request.user,
            title=title,
            description=description,
            location_name=location_name,
            latitude=latitude,
            longitude=longitude,
            hazard_photo=primary_photo,
            status='SUBMITTED',
        )

        # Create images in HazardReportImage
        for img in images:
            HazardReportImage.objects.create(
                report=report,
                image=img,
            )

        # Parse tags
        # Split by comma or hashtag
        tag_items = [t.strip().lstrip('#') for t in tags_raw.replace(';', ',').split(',') if t.strip()]
        for tag_name in tag_items:
            tag_name_clean = tag_name.strip()
            if tag_name_clean:
                tag_obj, _ = HazardTag.objects.get_or_create(name=tag_name_clean)
                report.tags.add(tag_obj)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({'success': True, 'redirect_url': reverse('home')})

        return redirect('home')

    # GET request
    all_tags = HazardTag.objects.all().order_by('name')
    return render(request, 'submit_report/submit_report.html', {
        'tags': all_tags,
    })
