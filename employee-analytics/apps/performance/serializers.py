
from rest_framework import serializers
from .models import Performance, Goal, Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model.
    """
    class Meta:
        model = Review
        fields = ['id', 'performance', 'category', 'rating', 'comments']
        read_only_fields = ['id']


class GoalSerializer(serializers.ModelSerializer):
    """
    Serializer for Goal model.
    """
    employee_name = serializers.ReadOnlyField(source='employee.full_name')

    class Meta:
        model = Goal
        fields = [
            'id', 'employee', 'employee_name', 'title', 'description',
            'start_date', 'target_date', 'completion_date', 'status', 'progress'
        ]
        read_only_fields = ['id']


class PerformanceSerializer(serializers.ModelSerializer):
    """
    Serializer for Performance model.
    """
    employee_name = serializers.ReadOnlyField(source='employee.full_name')
    employee_id = serializers.ReadOnlyField(source='employee.employee_id')
    reviewer_name = serializers.ReadOnlyField(source='reviewer.full_name')
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Performance
        fields = [
            'id', 'employee', 'employee_name', 'employee_id',
            'reviewer', 'reviewer_name', 'review_date',
            'performance_score', 'goals_achievement', 'comments', 'status', 'reviews'
        ]
        read_only_fields = ['id']


class PerformanceDetailSerializer(PerformanceSerializer):
    """
    Detailed serializer for Performance model with goal information.
    """
    goals = GoalSerializer(source='employee.goals', many=True, read_only=True)

    class Meta(PerformanceSerializer.Meta):
        fields = PerformanceSerializer.Meta.fields + ['goals']


class PerformanceSummarySerializer(serializers.Serializer):
    """
    Serializer for performance summary statistics.
    """
    total_reviews = serializers.IntegerField()
    avg_performance_score = serializers.DecimalField(max_digits=3, decimal_places=1)
    avg_goals_achievement = serializers.DecimalField(max_digits=5, decimal_places=2)
    excellent_count = serializers.IntegerField()
    good_count = serializers.IntegerField()
    average_count = serializers.IntegerField()
    needs_improvement_count = serializers.IntegerField()
