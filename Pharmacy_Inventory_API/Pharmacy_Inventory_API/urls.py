from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Schema View for API documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Pharmacy Inventory API",
      default_version='v1',
      description="API documentation for Pharmacy Inventory Management System",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Authentication URLs (built-in Django auth for templates)
    path("core/", include("django.contrib.auth.urls")),
    
    # Template-based authentication views
    path('auth/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='template_login'),
    path('auth/logout/', auth_views.LogoutView.as_view(next_page='/'), name='template_logout'),
    
    # Core app URLs (includes both template and API endpoints)
    path('', include('core.urls')),
    
    # API Endpoints
    path('api/medicines/', include('medicines.urls')),
    path('api/prescriptions/', include('prescriptions.urls')),
    path('api/alerts/', include('alerts.urls')),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Debug toolbar
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass