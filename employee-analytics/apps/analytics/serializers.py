
from rest_framework import serializers


class EmployeeStatsSerializer(serializers.Serializer):
    """
    Serializer for employee statistics.
    """
    total_employees = serializers.IntegerField()
    new_hires_this_month = serializers.IntegerField()


class DepartmentStatsSerializer(serializers.Serializer):
    """
    Serializer for department statistics.
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    employee_count = serializers.IntegerField()
    avg_salary = serializers.DecimalField(max_digits=10, decimal_places=2)


class AttendanceStatsSerializer(serializers.Serializer):
    """
    Serializer for attendance statistics.
    """
    total_records = serializers.IntegerField()
    present_count = serializers.IntegerField()
    late_count = serializers.IntegerField()
    absent_count = serializers.IntegerField()
    avg_hours_worked = serializers.DecimalField(max_digits=5, decimal_places=2)


class PerformanceStatsSerializer(serializers.Serializer):
    """
    Serializer for performance statistics.
    """
    total_reviews = serializers.IntegerField()
    avg_performance_score = serializers.DecimalField(max_digits=3, decimal_places=1)
    excellent_count = serializers.IntegerField()
    needs_improvement_count = serializers.IntegerField()


class DashboardSummarySerializer(serializers.Serializer):
    """
    Serializer for dashboard summary statistics.
    """
    employee_stats = EmployeeStatsSerializer()
    department_stats = DepartmentStatsSerializer(many=True)
    attendance_stats = AttendanceStatsSerializer()
    performance_stats = PerformanceStatsSerializer()
