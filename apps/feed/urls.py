from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('upvote/<int:report_id>/', views.toggle_upvote_view, name='feed_toggle_upvote'),
]
