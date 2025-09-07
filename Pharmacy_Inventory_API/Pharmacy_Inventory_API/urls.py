from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
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