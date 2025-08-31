"""
URL configuration for Pharmacy_Inventory_API project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from core.views import home, dashboard, login_view, logout_view, handler400, handler403, handler404, handler500, UserRegistrationView

# Custom 404 and 500 error handlers
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    
    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    
    # API Endpoints
    path('api/auth/', include('core.urls')),
    path('api/medicines/', include('medicines.urls')),
    path('api/prescriptions/', include('prescriptions.urls')),
    path('api/alerts/', include('alerts.urls')),
    
    # Home page
    path('', views.home, name='home'),
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