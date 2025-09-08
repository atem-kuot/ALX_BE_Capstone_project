from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        error_messages={
            'min_length': 'Password must be at least 8 characters long.',
            'blank': 'Password cannot be empty.',
        }
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        error_messages={'blank': 'Please confirm your password.'}
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password', 
                 'role', 'phone', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {
                'min_length': 4,
                'error_messages': {
                    'min_length': 'Username must be at least 4 characters long.',
                    'required': 'Username is required.'
                }
            },
            'email': {
                'required': True,
                'error_messages': {
                    'required': 'Email is required.',
                    'invalid': 'Enter a valid email address.'
                }
            },
            'first_name': {
                'required': True,
                'error_messages': {
                    'required': 'First name is required.'
                }
            },
            'last_name': {
                'required': True,
                'error_messages': {
                    'required': 'Last name is required.'
                }
            },
            'role': {
                'required': True,
                'error_messages': {
                    'required': 'Role is required.',
                    'invalid_choice': 'Invalid role selected.'
                }
            },
            'phone': {
                'required': False,
                'allow_blank': True,
                'error_messages': {
                    'invalid': 'Enter a valid phone number.'
                }
            }
        }
    def validate_username(self, value):
        """Validate username is unique and doesn't contain restricted characters."""
        if not value.isalnum():
            raise serializers.ValidationError("Username can only contain alphanumeric characters.")
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value.lower()

    def validate_email(self, value):
        """Validate email is unique and properly formatted."""
        value = value.lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_phone(self, value):
        """Validate phone number format if provided."""
        if not value:  # Phone is optional
            return value
            
        # Basic phone number validation (customize based on your needs)
        if not value.replace('+', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Enter a valid phone number.")
        return value

    def validate_password(self, value):
        """Validate password strength."""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        return value

    def validate(self, data):
        """Cross-field validation."""
        # Check if passwords match
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
            
        # Add any additional cross-field validations here
        return data

    def create(self, validated_data):
        """Create and return a new user with encrypted password."""
        # Remove confirm_password from validated_data
        validated_data.pop('confirm_password', None)
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            phone=validated_data.get('phone', '')
        )
        
        # Set password (hashed)
        user.set_password(validated_data['password'])
        user.save()
        
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        error_messages={
            'blank': 'Username is required.',
            'required': 'Username is required.'
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        error_messages={
            'blank': 'Password is required.',
            'required': 'Password is required.'
        }
    )
    
    def validate_username(self, value):
        """Normalize username to lowercase."""
        return value.lower()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        # Basic validation
        if not username or not password:
            raise serializers.ValidationError({
                'non_field_errors': ['Both username and password are required.']
            })
            
        # Prevent timing attacks
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        
        if not user:
            raise serializers.ValidationError({
                'non_field_errors': ['Invalid username or password.']
            })
            
        if not user.is_active:
            raise serializers.ValidationError({
                'non_field_errors': ['This account is inactive.']
            })
            
        data['user'] = user
        return data

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                    return data
                raise serializers.ValidationError("User account is disabled.")
            raise serializers.ValidationError("Invalid credentials.")
        raise serializers.ValidationError("Must include username and password.")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'phone', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('date_joined',)
