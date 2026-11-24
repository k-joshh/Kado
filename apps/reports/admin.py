from django.contrib import admin
from .models import HazardTag, HazardReport, HazardReportImage, ReportUpdate, ReportUpvote

class HazardReportImageInline(admin.TabularInline):
    model = HazardReportImage
    extra = 1

class ReportUpdateInline(admin.StackedInline):
    model = ReportUpdate
    extra = 0

@admin.register(HazardReport)
class HazardReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'tracking_token', 'status', 'location_name', 'reporter', 'created_at')
    list_filter = ('status', 'tags', 'created_at')
    search_fields = ('title', 'tracking_token', 'location_name', 'description')
    inlines = [HazardReportImageInline, ReportUpdateInline]

@admin.register(HazardTag)
class HazardTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(HazardReportImage)
class HazardReportImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'image', 'created_at')

@admin.register(ReportUpdate)
class ReportUpdateAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'author', 'status_milestone', 'created_at')

@admin.register(ReportUpvote)
class ReportUpvoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'user', 'created_at')
