
from django.contrib import admin
from .models import Employee, Department, Position


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'min_salary', 'max_salary']
    list_filter = ['department', 'title']
    search_fields = ['title', 'description']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'first_name', 'last_name', 'get_department_name', 'get_position_title', 'is_active']
    list_filter = ['department', 'position', 'gender', 'is_active']
    search_fields = ['first_name', 'last_name', 'employee_id', 'email']
    readonly_fields = ['employee_id']

    def get_department_name(self, obj):
        return obj.department.name if obj.department else "N/A"
    get_department_name.short_description = 'Department'

    def get_position_title(self, obj):
        return obj.position.title if obj.position else "N/A"
    get_position_title.short_description = 'Position'
