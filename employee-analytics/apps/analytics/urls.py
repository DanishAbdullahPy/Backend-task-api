
from django.urls import path
from .views import health_check, dashboard_summary

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('dashboard/', dashboard_summary, name='dashboard_summary'),
]
