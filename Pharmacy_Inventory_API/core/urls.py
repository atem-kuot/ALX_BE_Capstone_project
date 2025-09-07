from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home page
    path('', views.HomeView.as_view(), name='home'),

    # Template-based authentication (for rendering HTML forms)
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),

    # API endpoints for authentication
    path('api/auth/login/', views.UserLoginAPIView.as_view(), name='api_login'),
    path('api/auth/register/', views.UserRegistrationAPIView.as_view(), name='api_register'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]
