
from django.contrib import admin
from .models import Performance, Goal, Review


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['get_employee_name', 'review_date', 'performance_score', 'goals_achievement', 'status']
    list_filter = ['status', 'review_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    date_hierarchy = 'review_date'

    def get_employee_name(self, obj):
        return obj.employee.full_name if obj.employee else "N/A"
    get_employee_name.short_description = 'Employee'

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['employee', 'title', 'status', 'progress', 'target_date']
    list_filter = ['status']
    search_fields = ['employee__first_name', 'employee__last_name', 'title']
    date_hierarchy = 'target_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['get_performance_employee', 'category', 'rating']
    list_filter = ['category']
    search_fields = ['performance__employee__first_name', 'performance__employee__last_name', 'category']

    def get_performance_employee(self, obj):
        return obj.performance.employee.full_name if obj.performance and obj.performance.employee else "N/A"
    get_performance_employee.short_description = 'Performance Employee'
