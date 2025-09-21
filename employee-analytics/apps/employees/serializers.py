
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Employee, Department, Position


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Department model with employee count.
    """
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'employee_count']
        read_only_fields = ['id']

    def get_employee_count(self, obj):
        """Get count of active employees in the department."""
        return obj.employees.filter(is_active=True).count()


class PositionSerializer(serializers.ModelSerializer):
    """
    Serializer for Position model.
    """
    department_name = serializers.ReadOnlyField(source='department.name')
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = ['id', 'title', 'department', 'department_name', 'description', 
                 'min_salary', 'max_salary', 'employee_count']
        read_only_fields = ['id']

    def get_employee_count(self, obj):
        """Get count of employees in this position."""
        return obj.employees.filter(is_active=True).count()


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Employee model.
    """
    full_name = serializers.ReadOnlyField()
    department_name = serializers.ReadOnlyField(source='department.name')
    position_title = serializers.ReadOnlyField(source='position.title')
    manager_name = serializers.ReadOnlyField(source='manager.full_name')

    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'user', 'first_name', 'last_name', 'full_name',
            'gender', 'email', 'phone', 'department', 'department_name',
            'position', 'position_title', 'hire_date', 'salary', 'manager', 
            'manager_name', 'is_active', 'profile_image'
        ]
        read_only_fields = ['id']


class EmployeeDetailSerializer(EmployeeSerializer):
    """
    Detailed serializer for Employee model with nested relationships.
    """
    user_details = UserSerializer(source='user', read_only=True)
    department_details = DepartmentSerializer(source='department', read_only=True)
    position_details = PositionSerializer(source='position', read_only=True)
    manager_details = EmployeeSerializer(source='manager', read_only=True)

    class Meta(EmployeeSerializer.Meta):
        fields = EmployeeSerializer.Meta.fields + [
            'user_details', 'department_details', 'position_details', 'manager_details'
        ]


class DepartmentSummarySerializer(serializers.Serializer):
    """
    Serializer for department summary statistics.
    """
    department_id = serializers.IntegerField()
    department_name = serializers.CharField()
    employee_count = serializers.IntegerField()
    avg_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    min_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
