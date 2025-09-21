
from django.contrib import admin
from .models import Attendance, TimeLog


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'check_in', 'check_out', 'hours_worked']
    list_filter = ['status', 'date']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    date_hierarchy = 'date'


@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    list_display = ['attendance', 'log_type', 'timestamp']
    list_filter = ['log_type']
    search_fields = ['attendance__employee__first_name', 'attendance__employee__last_name']
    date_hierarchy = 'timestamp'
