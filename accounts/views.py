from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import ForgotPasswordSerializer, RegisterSerializer, ResetPasswordSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListCreateAPIView
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated

#Forget password APIVIEW

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Profile             
from .serializers import ProfileSerializer
from .models import Profile
from .serializers import ProfileSerializer


from rest_framework import viewsets
from .models import Reservation
from .serializers import ReservationSerializer




class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'

class ProfileDetailAPIView(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Profile, pk=pk)
        obj.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "Authenticated!"})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer



class ProfileListCreateAPIView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)



#change password and reset password

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Forget password APIVIEW

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password reset link sent to email."})
        return Response(serializer.errors, status=400)


#Reset password

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password has been reset."})
        return Response(serializer.errors, status=400)

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
















