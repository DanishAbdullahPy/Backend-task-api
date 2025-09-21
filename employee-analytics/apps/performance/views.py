
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Avg, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Performance, Goal, Review
from .serializers import (
    PerformanceSerializer, PerformanceDetailSerializer, 
    GoalSerializer, ReviewSerializer, PerformanceSummarySerializer
)


class PerformanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing performance reviews.

    Provides CRUD operations for Performance model with filtering capabilities
    by employee and review date range.
    """
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'status', 'review_date']
    search_fields = [
        'employee__first_name', 'employee__last_name', 
        'employee__employee_id', 'comments'
    ]
    ordering_fields = ['review_date', 'performance_score', 'goals_achievement']
    ordering = ['-review_date']

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.

        Returns:
            PerformanceDetailSerializer: For retrieve action (single performance)
            PerformanceSerializer: For all other actions
        """
        if self.action == 'retrieve':
            return PerformanceDetailSerializer
        return PerformanceSerializer

    def get_queryset(self):
        """
        Get the list of performance reviews for this view.

        Returns:
            QuerySet: Filtered list of performance reviews based on query parameters
        """
        queryset = Performance.objects.all()
        employee_id = self.request.query_params.get('employee_id', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        # Filter by employee ID if provided
        if employee_id:
            queryset = queryset.filter(employee__employee_id=employee_id)

        # Filter by start date if provided
        if start_date:
            queryset = queryset.filter(review_date__gte=start_date)

        # Filter by end date if provided
        if end_date:
            queryset = queryset.filter(review_date__lte=end_date)

        # Optimize query by selecting related employee and reviewer data
        return queryset.select_related('employee', 'reviewer')

    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        """
        Add a detailed review to a performance record.

        Args:
            request: HTTP request containing category, rating, and comments
            pk: Primary key of the performance record

        Returns:
            Response: JSON response with the created review
        """
        performance = self.get_object()

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(performance=performance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoalViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing employee goals.

    Provides CRUD operations for Goal model.
    """
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'status']
    search_fields = ['employee__first_name', 'employee__last_name', 'title', 'description']
    ordering_fields = ['target_date', 'start_date', 'progress']
    ordering = ['-target_date']


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing detailed reviews.

    Provides CRUD operations for Review model.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['performance', 'category']
    search_fields = ['performance__employee__first_name', 'performance__employee__last_name', 'comments']
    ordering_fields = ['category', 'rating']
    ordering = ['category']


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def performance_summary(request):
    """
    Get performance statistics summary.

    Calculates and returns performance review statistics for a given date range,
    including counts by status and aggregated score data.

    Args:
        request: HTTP request with optional start_date and end_date parameters

    Returns:
        Response: JSON response with performance statistics
    """
    # Get query parameters for date filtering
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    # Build base query
    queryset = Performance.objects.all()

    # Apply date filters if provided
    if start_date:
        queryset = queryset.filter(review_date__gte=start_date)

    if end_date:
        queryset = queryset.filter(review_date__lte=end_date)

    # Calculate statistics
    total_reviews = queryset.count()
    avg_performance_score = queryset.aggregate(Avg('performance_score'))['performance_score__avg'] or 0
    avg_goals_achievement = queryset.aggregate(Avg('goals_achievement'))['goals_achievement__avg'] or 0

    excellent_count = queryset.filter(status='excellent').count()
    good_count = queryset.filter(status='good').count()
    average_count = queryset.filter(status='average').count()
    needs_improvement_count = queryset.filter(status='needs_improvement').count()

    # Build response data
    data = {
        'total_reviews': total_reviews,
        'avg_performance_score': round(avg_performance_score, 1),
        'avg_goals_achievement': round(avg_goals_achievement, 2),
        'excellent_count': excellent_count,
        'good_count': good_count,
        'average_count': average_count,
        'needs_improvement_count': needs_improvement_count
    }

    serializer = PerformanceSummarySerializer(data=data)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
