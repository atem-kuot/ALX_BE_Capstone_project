from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .permissions import IsAdmin


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

@login_required
def dashboard(request):
    """Render the dashboard page"""
    context = {
        'title': 'Dashboard',
        'active_page': 'dashboard',
    }
    return render(request, 'core/dashboard.html', context)

def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.POST.get('next') or 'dashboard'
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    """Handle user logout"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('HomeView')

# Error Handlers
def handler404(request, template_name='errors/404.html'):
    """
    404 Error handler
    """
    context = {
        'title': 'Page Not Found',
        'error_code': 404,
        'error_message': 'The page you are looking for does not exist.'
    }
    return render(request, template_name, context, status=404)

def handler500(request, template_name='core/errors/500.html'):
    """
    500 Error handler
    """
    context = {
        'title': 'Server Error',
        'error_code': 500,
        'error_message': 'An error occurred while processing your request.'
    }
    return render(request, template_name, context, status=500)

def handler403(request, template_name='core/errors/403.html'):
    """
    403 Error handler
    """
    context = {
        'title': 'Permission Denied',
        'error_code': 403,
        'error_message': 'You do not have permission to access this page.'
    }
    return render(request, template_name, context, status=403)

def handler400(request, template_name='core/errors/400.html'):
    """
    400 Error handler
    """
    context = {
        'title': 'Bad Request',
        'error_code': 400,
        'error_message': 'The request could not be processed.'
    }
    return render(request, template_name, context, status=400)

class UserRegistrationView(APIView):
    permission_classes = []

    def get(self, request):
        """Render HTML registration page"""
        return render(request, 'register.html')

    def post(self, request):
        """Handle registration API request"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = []

    def get(self, request):
        """Render HTML login page"""
        return render(request, 'core/login.html')

    def post(self, request):
        """Handle login API request"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            refresh = RefreshToken.for_user(user)

            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

