from django.shortcuts import render
from rest_framework.decorators import api_view
from account.api.serializers import RegistrationSerializer
from rest_framework.response import Response
# from account.api import signals
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

@api_view(['POST'])
def register_view(request):
    data = {}
    
    if(request.method == 'POST'):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            created_user = serializer.save() # saves annd returns user(account)

            data['response'] = 'Account created successfully!'
            data['username'] = created_user.username
            data['email'] = created_user.email
            
            try:
                refresh_token = RefreshToken.for_user(created_user)
                data['token'] = {
                    'refresh_token': str(refresh_token),
                    'access_token': str(refresh_token.access_token)
                }
                # data['token'] = Token.objects.get(user=created_user).key
            except Token.DoesNotExist:
                Token.objects.create(user=created_user)

            return Response(data)
        else:
            data = serializer.errors
        
        return Response(data)
    
    return Response({'error': 'Method not allowed!'})


@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete() # deletes token for the user

    return Response(status=status.HTTP_200_OK)