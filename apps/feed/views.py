import json
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from apps.reports.models import HazardReport, ReportUpvote


def serialize_report(report, current_user=None):
    images = [img.image.url for img in report.images.all()]
    if not images and report.hazard_photo:
        images = [report.hazard_photo.url]

    first_image = images[0] if images else None

    reporter_name = "Anonymous"
    if report.reporter:
        full_name = f"{report.reporter.first_name} {report.reporter.last_name}".strip()
        reporter_name = full_name if full_name else report.reporter.email

    updates_data = []
    for u in report.updates.all().order_by('-created_at'):
        author_name = f"{u.author.first_name} {u.author.last_name}".strip() or u.author.email
        updates_data.append({
            'id': u.id,
            'author_name': author_name,
            'created_at': u.created_at.strftime('%Y/%m/%d %I:%M:%S %p'),
            'remarks': u.remarks,
            'status_milestone': u.get_status_milestone_display() if u.status_milestone else '',
            'photo_url': u.update_photo.url if u.update_photo else None,
        })

    upvotes_count = report.upvotes.count()
    user_has_upvoted = False
    if current_user and current_user.is_authenticated:
        user_has_upvoted = report.upvotes.filter(user=current_user).exists()

    status_color_map = {
        'SUBMITTED': '#EA580C',
        'SCHEDULED': '#3B82F6',
        'RESOLVED': '#10B981',
    }

    return {
        'id': report.id,
        'tracking_token': report.tracking_token,
        'title': report.title,
        'description': report.description,
        'location_name': report.location_name or f"{report.latitude:.4f}, {report.longitude:.4f}",
        'latitude': float(report.latitude),
        'longitude': float(report.longitude),
        'status': report.status,
        'status_display': report.get_status_display(),
        'status_color': status_color_map.get(report.status, '#EA580C'),
        'created_at_formatted': report.created_at.strftime('%Y/%m/%d, %I:%M %p'),
        'created_at_detailed': report.created_at.strftime('%Y/%m/%d, %I:%M:%S %p'),
        'created_at_timestamp': report.created_at.timestamp(),
        'updated_at_timestamp': report.updated_at.timestamp(),
        'reporter_name': reporter_name,
        'tags': [t.name for t in report.tags.all()],
        'tags_display': ', '.join([t.name for t in report.tags.all()]),
        'images': images,
        'first_image': first_image,
        'upvotes_count': upvotes_count,
        'user_has_upvoted': user_has_upvoted,
        'updates': updates_data,
        'updates_count': len(updates_data),
    }


@login_required(login_url='login')
def feed_view(request):
    reports_qs = (
        HazardReport.objects.all()
        .prefetch_related('tags', 'images', 'updates__author', 'upvotes')
        .select_related('reporter')
        .order_by('-created_at')
    )

    reports_data = [serialize_report(r, request.user) for r in reports_qs]

    return render(request, 'feed/feed.html', {
        'reports_data': reports_data,
    })


@login_required(login_url='login')
@require_POST
def toggle_upvote_view(request, report_id):
    report = get_object_or_404(HazardReport, id=report_id)
    existing_upvote = ReportUpvote.objects.filter(report=report, user=request.user)

    if existing_upvote.exists():
        existing_upvote.delete()
        upvoted = False
    else:
        ReportUpvote.objects.create(report=report, user=request.user)
        upvoted = True

    count = report.upvotes.count()
    return JsonResponse({
        'success': True,
        'upvoted': upvoted,
        'upvotes_count': count,
        'report_id': report.id,
    })
