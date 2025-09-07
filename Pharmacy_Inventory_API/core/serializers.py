from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)  
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password', 'role', 'phone', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': True}
        }
        
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
        
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
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
