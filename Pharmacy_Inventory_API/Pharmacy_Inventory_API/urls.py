"""
URL configuration for Pharmacy_Inventory_API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/core/', include('core.urls')),
    path('api/medicines/', include('medicines.urls')),
    path('api/prescriptions/', include('prescriptions.urls')),
    path('api/alerts/', include('alerts.urls')),
]from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("""
    <h1>🏥 Pharmacy Management API</h1>
    <p>API is running successfully!</p>
    <ul>
        <li><a href="/api/auth/">Login</a></li>
        <li><a href="/admin/">Admin</a></li>
    </ul>
    """)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('core.urls')),
    path('api/medicines/', include('medicines.urls')),
    path('api/prescriptions/', include('prescriptions.urls')),
    path('api/alerts/', include('alerts.urls')),
]
