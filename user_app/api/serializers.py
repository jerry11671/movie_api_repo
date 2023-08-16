from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={'input_type':'password'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def save(self):
        password2 = self.validated_data['password2']
        password = self.validated_data['password']
        
        if password2 != password:
            raise serializers.ValidationError({'error': 'Both passwords should be the same!!'})
        
        if User.objects.filter(email=self.validated_data['email']):
            raise serializers.ValidationError({'error':'Email already exists!'})
        
        # To create an instance of the User class
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        
        return account
        
        