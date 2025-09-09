from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer

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


class UserRegistrationAPIView(APIView):
    """API endpoint for user registration"""
    permission_classes = []
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    """API endpoint for user login"""
    permission_classes = []
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Template-based views for rendering HTML forms
class UserRegistrationView(APIView):
    permission_classes = []
    
    def get(self, request):
        form = UserCreationForm()
        return render(request, "core/register.html", {"form": form})

    def post(self, request):
        # Handle both form data and JSON data
        if request.content_type == 'application/json':
            # API call
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Form submission
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("login")
            return render(request, "core/register.html", {"form": form})


class UserLoginView(LoginView):
    """Template-based login view"""
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
    next_page = "/"


# Add a view to show login template
def login_page(request):
    return render(request, 'core/login.html')


def register_page(request):
    return render(request, 'core/register.html')
    
    
