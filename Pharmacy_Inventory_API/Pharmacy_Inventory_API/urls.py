"""
URL configuration for Pharmacy_Inventory_API project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from core.views import dashboard, login_view, logout_view

# Custom 404 and 500 error handlers
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    
    # API Endpoints
    path('api/auth/', include('core.urls')),
    path('api/medicines/', include('medicines.urls')),
    path('api/prescriptions/', include('prescriptions.urls')),
    path('api/alerts/', include('alerts.urls')),
    
    # Home page - redirect to dashboard if authenticated, otherwise to login
    path('', lambda request: dashboard(request) if request.user.is_authenticated else login_view(request), name='home'),
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