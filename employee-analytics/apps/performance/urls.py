
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PerformanceViewSet, GoalViewSet, ReviewViewSet, performance_summary

router = DefaultRouter()
router.register(r'performances', PerformanceViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('summary/performance/', performance_summary, name='performance_summary'),
]
