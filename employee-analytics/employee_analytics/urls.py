
from django.contrib import admin  # Django admin interface
from django.urls import path, include  # URL routing functionality
from drf_yasg.views import get_schema_view  # Swagger schema view generator
from drf_yasg import openapi  # OpenAPI specification support
from rest_framework import permissions  # REST framework permissions
from apps.analytics.views import health_check  # Health check endpoint

# Swagger/OpenAPI schema view configuration
# This defines the API documentation accessible via Swagger UI and ReDoc
schema_view = get_schema_view(
   openapi.Info(
      title="Employee Analytics API",  # API title
      default_version='v1',  # Default API version
      description="API documentation for Employee Analytics System",  # API description
      terms_of_service="https://www.example.com/policies/terms/",  # Terms of service URL
      contact=openapi.Contact(email="contact@example.com"),  # Contact information
      license=openapi.License(name="BSD License"),  # License information
   ),
   public=True,  # Make the schema public (accessible without authentication)
   permission_classes=[permissions.AllowAny],  # Allow anyone to access the schema
)

from django.views.generic import RedirectView  # Generic view for redirecting URLs

# URL patterns for the application
urlpatterns = [
    # Redirect root URL to Swagger documentation
    path('', RedirectView.as_view(url='swagger/', permanent=True)),
    
    # Django admin interface URL
    path('admin/', admin.site.urls),
    
    # Employee management API URLs
    path('api/', include('apps.employees.urls')),
    
    # Attendance tracking API URLs
    path('api/', include('apps.attendance.urls')),
    
    # Performance evaluation API URLs
    path('api/', include('apps.performance.urls')),
    
    # Analytics and reporting API URLs
    path('api/', include('apps.analytics.urls')),
    
    # Authentication API URLs
    path('api/auth/', include('rest_framework.urls')),
    
    # Swagger UI documentation endpoint
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # ReDoc documentation endpoint
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Health check endpoint for monitoring
    path('health/', health_check, name='health_check'),
]
