from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_app.models import UserData
from user_app.serializers import UserSerializer
from django.contrib.auth.hashers import make_password ,check_password
import jwt
from django.conf import settings 
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def user_registration(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():

        # Hash the password before saving the user
        password = request.data.get('password')
        hashed_password = make_password(password)
        serializer.validated_data['password'] = hashed_password

        # Check for unique phone number
        phone_number = serializer.validated_data.get('phone_number')
        if UserData.objects.filter(phone_number=phone_number).exists():
            return Response({'error': 'Phone number already registered'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')

    try:
        user = UserData.objects.get(phone_number=phone_number)
    except UserData.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password,user.password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

   # Generate JWT token
    refresh = RefreshToken.for_user(user)
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

    return Response({'token': token, 'user': UserSerializer(user).data})
