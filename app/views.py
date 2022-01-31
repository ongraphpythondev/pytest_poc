from django.views.decorators.csrf import csrf_exempt
from rest_framework import response
from django.contrib.auth.models import auth , User
from rest_framework.views import APIView
from .serializers import   UserSerializer ,ChangepasswordSerializer , ResetpasswordSerializer
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password



class Login(APIView):

    @csrf_exempt
    def post(self, request, format=None):
        data = self.request.data
        if request.user.is_authenticated :
            return Response({"stat" : "User is already logged in"} ,status = status.HTTP_401_UNAUTHORIZED)
        username = data.get('username', None)
        password = data.get('password', None)
        user =  auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)

            return Response({"stat" : "User logged in"} , status=status.HTTP_200_OK)
        else:
            return Response({"stat" : "User not found"},status=status.HTTP_404_NOT_FOUND)

class Registration(APIView):

    @csrf_exempt
    def post(self , request):
        serializer = UserSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if not request.user :
            return Response({"stat" : "please login first"} , status=status.HTTP_200_OK)
        auth.logout(request)
        return Response({"status":"user logged out"},status=status.HTTP_200_OK)


class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self , request , pk):
        user = User.objects.get(pk = pk)
        if user is None:
            return response({"Not found" : "user not found"} , status=status.HTTP_400_BAD_REQUEST)
        if user.username != request.user.username:
            return response({"Not found" : "user not login with correct account"} , status=status.HTTP_400_BAD_REQUEST)
        if not check_password(request.data.get("old_password"),user.password):
            return response({"error" : "old password not match"} , status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("password") != request.data.get("password2"):
            return response({"Not match" : "password and password2 did not match"} , status=status.HTTP_400_BAD_REQUEST)


        # user.set_password(request.data.get("password"))
        data = {
            "password" : make_password(request.data.get("password"))
            }
        username = user.username
        serializer = ChangepasswordSerializer(user , data = data , partial=True)
        if serializer.is_valid():
            serializer.save()
            user =  auth.authenticate(username=username, password=request.data.get("password"))
            if user is not None:
                auth.login(request, user)
            return Response({"new_password" : request.data.get("password")} , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordView(APIView):


    @csrf_exempt
    def post(self , request ):
        user = User.objects.filter(username = request.data.get("username")).first()
        if user is None:
            return response({"Not found" : "user not found"} , status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("password") != request.data.get("password2"):
            return response({"Not match" : "password and password2 did not match"} , status=status.HTTP_400_BAD_REQUEST)


        # user.set_password(request.data.get("password"))
        data = {
            "password" : make_password(request.data.get("password"))
            }
        username = user.username
        serializer = ResetpasswordSerializer(user , data = data , partial=True)
        if serializer.is_valid():
            serializer.save()
            user =  auth.authenticate(username=username, password=request.data.get("password"))
            if user is not None:
                auth.login(request, user)
            return Response({"new_password" : request.data.get("password")} , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)