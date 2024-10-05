from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
import jwt
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from django.contrib.auth import authenticate

from api.models import Product
from api.pagination import ProductDetailPagination, ProductListPagination
from api.serializers import ProductSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from api.filters import ProductFilter
# Create your views here.


class Register(APIView):
    # pass
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        else:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
"""        user = User.objects.filter(username=username).first()
        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid password")

        payload = {
            'id': user.id,
            'exp' :timezone.now() + timezone.timedelta(minutes=60),
            'iat' :timezone.now()
        }
        token = jwt.encode(payload,'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return Response({
            'jwt': token
        }
            
        )"""


class ProductListViewset(generics.ListCreateAPIView):  # list and create endpoint
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = ProductListPagination
    filter_backends = (SearchFilter,DjangoFilterBackend,OrderingFilter)
    filter_class = ProductFilter
    search_fields = ("name", "description")
    ordering_fields = ('price','created_at')
    
    def perform_create(self, serializer):
        serializer.save()


class ProductDetailViewset(
    generics.RetrieveUpdateDestroyAPIView
):  # retrieve, update and delete endpoint
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductDetailPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
