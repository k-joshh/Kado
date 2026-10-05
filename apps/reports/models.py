from django.db import models
from django.conf import settings

class HazardCategory(models.Model):
    name = models.CharField(max_length=100)
    assigned_office = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class HazardReport(models.Model):
    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted'),
        ('SCHEDULED', 'Scheduled for Inspection'),
        ('RESOLVED', 'Resolved'),
    ]

    tracking_token = models.CharField(max_length=32, unique=True)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    category = models.ForeignKey(HazardCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    title = models.CharField(max_length=150)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    hazard_photo = models.ImageField(upload_to='hazards/initial/%Y/%m/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class ReportUpdate(models.Model):
    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted'),
        ('SCHEDULED', 'Scheduled for Inspection'),
        ('RESOLVED', 'Resolved'),
    ]

    report = models.ForeignKey(HazardReport, on_delete=models.CASCADE, related_name='updates')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='report_updates')
    remarks = models.TextField()
    update_photo = models.ImageField(upload_to='hazards/updates/%Y/%m/', null=True, blank=True)
    status_milestone = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update by {self.author.email} on Report #{self.report_id}"


class ReportUpvote(models.Model):
    report = models.ForeignKey(HazardReport, on_delete=models.CASCADE, related_name='upvotes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='report_upvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} upvoted #{self.report_id}"