from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

# from user_app import models

@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def register(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        # token = Token.objects.get(user=request.user).key
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            # print(account)
            
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email
            
            # token = Token.objects.get(user=account).key
            token = RefreshToken.for_user(account)
            # data['token'] = token
            data['token'] = {
                'refresh': str(token),
                'access': str(token.access_token)
            }
        
        else:
            data = serializer.errors
            
        return Response(data)
        
        
        

            # data['response'] = "User successfully created!"
            # data['token'] = token
            # data['Username'] = serializer.validated_data['username']
            # data['email'] = serializer.validated_data['email']

