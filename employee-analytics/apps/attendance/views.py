
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Avg, Count, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from datetime import datetime

from .models import Attendance, TimeLog
from .serializers import AttendanceSerializer, TimeLogSerializer, AttendanceSummarySerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing attendance records.

    Provides CRUD operations for Attendance model with filtering capabilities
    by employee, date range, and status.
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'status', 'date']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id', 'notes']
    ordering_fields = ['date', 'check_in', 'check_out', 'hours_worked']
    ordering = ['-date']

    def get_queryset(self):
        """
        Get the list of attendance records for this view.

        Returns:
            QuerySet: Filtered list of attendance records based on query parameters
        """
        queryset = Attendance.objects.all()
        employee_id = self.request.query_params.get('employee_id', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        # Filter by employee ID if provided
        if employee_id:
            queryset = queryset.filter(employee__employee_id=employee_id)

        # Filter by start date if provided
        if start_date:
            queryset = queryset.filter(date__gte=start_date)

        # Filter by end date if provided
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        # Optimize query by selecting related employee data
        return queryset.select_related('employee')

    @action(detail=False, methods=['post'])
    def check_in(self, request):
        """
        Check in an employee for the day.

        Args:
            request: HTTP request containing employee_id

        Returns:
            Response: JSON response with check-in status
        """
        employee_id = request.data.get('employee_id')
        today = datetime.now().date()

        try:
            # Get or create attendance record for today
            attendance, created = Attendance.objects.get_or_create(
                employee_id=employee_id,
                date=today,
                defaults={'status': 'present'}
            )

            # Update check-in time
            attendance.check_in = datetime.now()
            attendance.save()

            # Create time log
            TimeLog.objects.create(
                attendance=attendance,
                log_type='check_in',
                timestamp=datetime.now()
            )

            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def check_out(self, request):
        """
        Check out an employee for the day.

        Args:
            request: HTTP request containing employee_id

        Returns:
            Response: JSON response with check-out status
        """
        employee_id = request.data.get('employee_id')
        today = datetime.now().date()

        try:
            # Get attendance record for today
            attendance = Attendance.objects.get(
                employee_id=employee_id,
                date=today
            )

            # Update check-out time
            attendance.check_out = datetime.now()

            # Calculate hours worked
            if attendance.check_in:
                diff = attendance.check_out - attendance.check_in
                hours_worked = round(diff.total_seconds() / 3600, 2)
                attendance.hours_worked = hours_worked

                # Calculate overtime if worked more than 8 hours
                if hours_worked > 8:
                    attendance.overtime_hours = round(hours_worked - 8, 2)

            attendance.save()

            # Create time log
            TimeLog.objects.create(
                attendance=attendance,
                log_type='check_out',
                timestamp=datetime.now()
            )

            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data)

        except Attendance.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'No attendance record found for today'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class TimeLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing time logs.

    Provides CRUD operations for TimeLog model.
    """
    queryset = TimeLog.objects.all()
    serializer_class = TimeLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['attendance', 'log_type']
    search_fields = ['attendance__employee__first_name', 'attendance__employee__last_name', 'notes']
    ordering_fields = ['timestamp']
    ordering = ['timestamp']


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def attendance_summary(request):
    """
    Get attendance statistics summary.

    Calculates and returns attendance statistics for a given date range,
    including counts by status and aggregated hours data.

    Args:
        request: HTTP request with optional start_date and end_date parameters

    Returns:
        Response: JSON response with attendance statistics
    """
    # Get query parameters for date filtering
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    # Build base query
    queryset = Attendance.objects.all()

    # Apply date filters if provided
    if start_date:
        queryset = queryset.filter(date__gte=start_date)

    if end_date:
        queryset = queryset.filter(date__lte=end_date)

    # Calculate statistics by attendance status
    total_records = queryset.count()
    present_count = queryset.filter(status='present').count()
    late_count = queryset.filter(status='late').count()
    early_leave_count = queryset.filter(status='early_leave').count()
    absent_count = queryset.filter(status='absent').count()
    leave_count = queryset.filter(status='leave').count()

    # Calculate aggregated hours data
    avg_hours_worked = queryset.aggregate(Avg('hours_worked'))['hours_worked__avg'] or 0
    total_overtime_hours = queryset.aggregate(Sum('overtime_hours'))['overtime_hours__sum'] or 0

    # Build response data structure
    data = {
        'total_records': total_records,
        'present_count': present_count,
        'late_count': late_count,
        'early_leave_count': early_leave_count,
        'absent_count': absent_count,
        'leave_count': leave_count,
        'avg_hours_worked': round(avg_hours_worked, 2),
        'total_overtime_hours': round(total_overtime_hours, 2)
    }

    serializer = AttendanceSummarySerializer(data=data)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
