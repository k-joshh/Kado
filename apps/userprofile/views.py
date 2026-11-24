from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.reports.models import HazardReport
from apps.feed.views import serialize_report

# Create your views here.
@login_required
def profile_view(request):
    user_reports_qs = (
        HazardReport.objects.filter(reporter=request.user)
        .prefetch_related('tags', 'images', 'updates__author', 'upvotes')
        .select_related('reporter')
        .order_by('-created_at')
    )

    my_reports = [serialize_report(r, request.user) for r in user_reports_qs]

    return render(request, 'userprofile/profile.html', {
        'my_reports': my_reports,
        'reports_count': len(my_reports),
    })
