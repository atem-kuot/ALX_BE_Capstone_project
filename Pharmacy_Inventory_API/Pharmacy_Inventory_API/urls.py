"""
URL configuration for Pharmacy_Inventory_API project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from core.views import dashboard, HomeView




urlpatterns = [

    # Admin
    path('admin/', admin.site.urls),
    path("core/", include("django.contrib.auth.urls")),

    # Authentication
    path('api/auth/login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('api/auth/logout/', views.LogoutView.as_view(next_page=HomeView), name='logout'),
    path('api/auth/register/', views.UserRegistrationView.as_view(), name='register'),

    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # API Endpoints
    path('', include('core.urls')),
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