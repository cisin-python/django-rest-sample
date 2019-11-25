"""Registration controller."""
# from django.views.generic import View
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework import status
from .serializers import LoginSerializer


class LoginAPIView(generics.GenericAPIView):
    """Login Api for the User Authentication."""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """Create user login."""
        data = {
            'msg': "Successfully logged in.",
        }
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            authenticated_user = serializer.validated_data.get(
                'authenticated_user')
            if authenticated_user:
                login(request, authenticated_user)
                data['id'] = authenticated_user.id
                data['username'] = authenticated_user.username
                data['email'] = authenticated_user.email
                data["status"] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data['msg'] = "Error"
            data["status"] = False
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    """Logout user."""

    queryset = []

    def get(self, request, format=None):
        """User logout."""
        data = {
            'msg': "Logged out.",
            'status': True
        }
        logout(request)
        return Response(data, status=status.HTTP_200_OK)
