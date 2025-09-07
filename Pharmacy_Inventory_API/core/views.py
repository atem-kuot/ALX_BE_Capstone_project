from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView

class HomeView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        context = {
            'system_name': 'Pharmacy Management System',
            'version': '1.0.0',
            'stats': {
                'medicines': 4800,
                'prescriptions': 100,
                'users': 10,
                'alerts': 10,
            },
            'features': [
                {'icon': '💊', 'title': 'Inventory Tracking', 'desc': 'Real-time medicine stock management.'},
                {'icon': '📄', 'title': 'Electronic Prescriptions', 'desc': 'E-prescription system for healthcare providers.'},
                {'icon': '🔔', 'title': 'Smart Alerts', 'desc': 'Get notified for low stock and expired items.'},
            ],
            'user_roles': [
                {'icon': '👨‍⚕️', 'role': 'Pharmacist', 'description': 'Manage medicines and prescriptions.'},
                {'icon': '👩‍⚕️', 'role': 'Doctor', 'description': 'Create and track prescriptions.'},
                {'icon': '🧑‍💼', 'role': 'Admin', 'description': 'Oversee system and manage staff.'},
            ]
        }
        return render(request, 'core/home.html', context)




class UserRegistrationView(APIView):
    permission_classes = []
    def get(self, request):
        form = UserCreationForm()
        return render(request, "core/register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("core/login")
        return render(request, "core/register.html", {"form": form})


class UserLoginView(LoginView):
    """Use built-in LoginView"""
    template_name = "core/login.html"
    authentication_form = AuthenticationForm

@login_required
def dashboard(request):
    context = {
        "title": "Dashboard",
        "active_page": "dashboard",
    }
    messages.info(request, f"Welcome back, {request.user.first_name}!")
    return render(request, "core/dashboard.html", context)

class UserLogoutView(LogoutView):
    """Use built-in LogoutView"""
    template_name = "core/logout.html"
    next_page = "core/home.html"



