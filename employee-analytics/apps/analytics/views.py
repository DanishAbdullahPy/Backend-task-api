
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Avg, Count, Min, Max, Sum
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

from apps.employees.models import Employee, Department
from apps.attendance.models import Attendance
from apps.performance.models import Performance


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """
    Health check endpoint.

    Provides a simple endpoint to check if the API is running and responsive.
    Returns current server status and timestamp.

    Args:
        request: HTTP request

    Returns:
        JsonResponse: JSON response with health status and timestamp
    """
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat()
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_summary(request):
    """
    Get dashboard summary statistics.

    Provides a comprehensive overview of the organization including:
    - Employee statistics
    - Department statistics
    - Attendance statistics
    - Performance statistics

    Args:
        request: HTTP request with optional date range parameters

    Returns:
        Response: JSON response with dashboard summary statistics
    """
    # Get query parameters for date filtering
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    # Employee statistics
    total_employees = Employee.objects.filter(is_active=True).count()
    new_hires_this_month = Employee.objects.filter(
        hire_date__gte=timezone.now().replace(day=1),
        is_active=True
    ).count()

    # Department statistics
    department_stats = Department.objects.annotate(
        employee_count=Count('employees', filter=models.Q(employees__is_active=True)),
        avg_salary=Avg('employees__salary', filter=models.Q(employees__is_active=True))
    ).order_by('-employee_count')

    # Attendance statistics
    attendance_queryset = Attendance.objects.all()
    if start_date:
        attendance_queryset = attendance_queryset.filter(date__gte=start_date)
    if end_date:
        attendance_queryset = attendance_queryset.filter(date__lte=end_date)

    attendance_stats = {
        'total_records': attendance_queryset.count(),
        'present_count': attendance_queryset.filter(status='present').count(),
        'late_count': attendance_queryset.filter(status='late').count(),
        'absent_count': attendance_queryset.filter(status='absent').count(),
        'avg_hours_worked': round(attendance_queryset.aggregate(Avg('hours_worked'))['hours_worked__avg'] or 0, 2),
    }

    # Performance statistics
    performance_queryset = Performance.objects.all()
    if start_date:
        performance_queryset = performance_queryset.filter(review_date__gte=start_date)
    if end_date:
        performance_queryset = performance_queryset.filter(review_date__lte=end_date)

    performance_stats = {
        'total_reviews': performance_queryset.count(),
        'avg_performance_score': round(performance_queryset.aggregate(Avg('performance_score'))['performance_score__avg'] or 0, 1),
        'excellent_count': performance_queryset.filter(status='excellent').count(),
        'needs_improvement_count': performance_queryset.filter(status='needs_improvement').count(),
    }

    # Build response data
    data = {
        'employee_stats': {
            'total_employees': total_employees,
            'new_hires_this_month': new_hires_this_month,
        },
        'department_stats': [
            {
                'id': dept.id,
                'name': dept.name,
                'employee_count': dept.employee_count,
                'avg_salary': round(dept.avg_salary or 0, 2)
            }
            for dept in department_stats
        ],
        'attendance_stats': attendance_stats,
        'performance_stats': performance_stats,
    }

    return Response(data)
