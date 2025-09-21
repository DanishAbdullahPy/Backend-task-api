
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        # Check if the object has a user attribute and if it matches the current user
        if hasattr(obj, 'user'):
            return obj.user == request.user

        # For Employee objects, check if the associated user matches the current user
        if hasattr(obj, 'employee') and hasattr(obj.employee, 'user'):
            return obj.employee.user == request.user

        # For objects that directly reference Employee
        if hasattr(obj, 'employee_id'):
            from apps.employees.models import Employee
            try:
                employee = Employee.objects.get(id=obj.employee_id)
                return employee.user == request.user
            except Employee.DoesNotExist:
                return False

        return False


class IsDepartmentManager(permissions.BasePermission):
    """
    Custom permission to only allow department managers to edit objects.
    """

    def has_permission(self, request, view):
        # Check if the user is a department manager
        if not request.user.is_authenticated:
            return False

        from apps.employees.models import Employee
        try:
            employee = Employee.objects.get(user=request.user)
            # Check if the employee is a manager (has subordinates)
            return employee.subordinates.exists()
        except Employee.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        # Check if the user is a manager of the department associated with the object
        if not request.user.is_authenticated:
            return False

        from apps.employees.models import Employee
        try:
            user_employee = Employee.objects.get(user=request.user)

            # For objects with a direct department reference
            if hasattr(obj, 'department'):
                return obj.department == user_employee.department and user_employee.subordinates.exists()

            # For objects with an employee that has a department
            if hasattr(obj, 'employee'):
                return obj.employee.department == user_employee.department and user_employee.subordinates.exists()

            # For Employee objects directly
            if hasattr(obj, 'department_id'):
                return obj.department_id == user_employee.department.id and user_employee.subordinates.exists()

        except Employee.DoesNotExist:
            return False

        return False


class IsHRUser(permissions.BasePermission):
    """
    Custom permission to only allow HR users to access certain views.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        from apps.employees.models import Employee
        try:
            employee = Employee.objects.get(user=request.user)
            return employee.department.name.lower() == 'human resources'
        except Employee.DoesNotExist:
            return False
