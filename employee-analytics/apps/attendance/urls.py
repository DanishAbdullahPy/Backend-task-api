
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, TimeLogViewSet, attendance_summary

router = DefaultRouter()
router.register(r'attendances', AttendanceViewSet)
router.register(r'time_logs', TimeLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('summary/attendance/', attendance_summary, name='attendance_summary'),
]
