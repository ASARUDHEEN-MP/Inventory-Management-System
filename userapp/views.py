from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from . import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
# create a user (registration)
class UserRegistration(generics.GenericAPIView):
    serializer_class = serializers.RegistarionSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # if the serializer is valid return the successfull response
            return Response({
                "message": 'User registration is successful...'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# login for the user
class UserLogin(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.Loginserializer  # Make sure this matches your LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            token_data = serializer.validated_data
            return Response(token_data, status=status.HTTP_200_OK)
        except ValidationError as e:  # Use ValidationError from DRF
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)

