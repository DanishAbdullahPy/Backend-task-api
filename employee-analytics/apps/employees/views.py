
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Avg, Count, Min, Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Employee, Department, Position
from .serializers import (
    UserSerializer, EmployeeSerializer, EmployeeDetailSerializer,
    DepartmentSerializer, PositionSerializer, DepartmentSummarySerializer
)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing employees.

    Provides CRUD operations for Employee model with filtering capabilities
    by department, position, and active status.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'position', 'is_active', 'gender']
    search_fields = ['first_name', 'last_name', 'employee_id', 'email']
    ordering_fields = ['last_name', 'first_name', 'hire_date', 'salary']
    ordering = ['last_name', 'first_name']

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.

        Returns:
            EmployeeDetailSerializer: For retrieve action (single employee)
            EmployeeSerializer: For all other actions
        """
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return EmployeeSerializer

    @action(detail=False, methods=['get'])
    def by_department(self, request):
        """
        Get employees grouped by department.

        Returns:
            Response: JSON response with employees grouped by department
        """
        departments = Department.objects.all()
        result = {}

        for dept in departments:
            employees = Employee.objects.filter(department=dept, is_active=True)
            serializer = EmployeeSerializer(employees, many=True)
            result[dept.name] = serializer.data

        return Response(result)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing departments.

    Provides CRUD operations for Department model.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get department statistics summary.

        Calculates and returns statistics for each department including:
        - Employee count
        - Average salary
        - Minimum salary
        - Maximum salary

        Args:
            request: HTTP request

        Returns:
            Response: JSON response with department statistics
        """
        departments = Department.objects.annotate(
            employee_count=Count('employees', filter=models.Q(employees__is_active=True)),
            avg_salary=Avg('employees__salary', filter=models.Q(employees__is_active=True)),
            min_salary=Min('employees__salary', filter=models.Q(employees__is_active=True)),
            max_salary=Max('employees__salary', filter=models.Q(employees__is_active=True))
        )

        serializer = DepartmentSummarySerializer(departments, many=True)
        return Response(serializer.data)


class PositionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing positions.

    Provides CRUD operations for Position model.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department']
    search_fields = ['title', 'description']
