
from rest_framework import serializers
from .models import Attendance, TimeLog


class TimeLogSerializer(serializers.ModelSerializer):
    """
    Serializer for TimeLog model.
    """
    class Meta:
        model = TimeLog
        fields = ['id', 'attendance', 'log_type', 'timestamp', 'notes']
        read_only_fields = ['id']


class AttendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for Attendance model.
    """
    employee_name = serializers.ReadOnlyField(source='employee.full_name')
    employee_id = serializers.ReadOnlyField(source='employee.employee_id')
    time_logs = TimeLogSerializer(many=True, read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_name', 'employee_id', 'date',
            'check_in', 'check_out', 'status', 'hours_worked',
            'overtime_hours', 'notes', 'time_logs'
        ]
        read_only_fields = ['id']


class AttendanceSummarySerializer(serializers.Serializer):
    """
    Serializer for attendance summary statistics.
    """
    total_records = serializers.IntegerField()
    present_count = serializers.IntegerField()
    late_count = serializers.IntegerField()
    early_leave_count = serializers.IntegerField()
    absent_count = serializers.IntegerField()
    leave_count = serializers.IntegerField()
    avg_hours_worked = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_overtime_hours = serializers.DecimalField(max_digits=5, decimal_places=2)
