from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponseServerError
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .permissions import IsAdmin

# Template Views
@login_required
def dashboard(request):
    """Render the dashboard page"""
    context = {
        'title': 'Dashboard',
        'active_page': 'dashboard',
    }
    return render(request, 'dashboard.html', context)

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
    
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    """Handle user logout"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

# Error Handlers
def handler404(request, exception, template_name='errors/404.html'):
    """
    404 Error handler
    """
    context = {
        'title': 'Page Not Found',
        'error_code': 404,
        'error_message': 'The page you are looking for does not exist.'
    }
    return render(request, template_name, context, status=404)

def handler500(request, template_name='errors/500.html'):
    """
    500 Error handler
    """
    context = {
        'title': 'Server Error',
        'error_code': 500,
        'error_message': 'An error occurred while processing your request.'
    }
    return render(request, template_name, context, status=500)

def handler403(request, exception, template_name='errors/403.html'):
    """
    403 Error handler
    """
    context = {
        'title': 'Permission Denied',
        'error_code': 403,
        'error_message': 'You do not have permission to access this page.'
    }
    return render(request, template_name, context, status=403)

def handler400(request, exception, template_name='errors/400.html'):
    """
    400 Error handler
    """
    context = {
        'title': 'Bad Request',
        'error_code': 400,
        'error_message': 'The request could not be processed.'
    }
    return render(request, template_name, context, status=400)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
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
# Create your views here.
