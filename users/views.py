from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from users.models import User
from users.permissions import IsAllowedUser
from .serializers import UserSerializer, CustomJWTSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = User.objects.filter(
            email__iexact=serializer.validated_data["email"]
        ).first()
        username = User.objects.filter(
            username__iexact=request.data["username"]
        ).first()

        return_conflict = {}

        if email:
            return_conflict.update({"email": ["email already registered."]})
        if username:
            return_conflict.update({"username": ["username already taken."]})

        if return_conflict:
            return Response(return_conflict, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAllowedUser]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, pk=user_id)
        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, pk=user_id)
        self.check_object_permissions(request, user)

        serializer = UserSerializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for key, value in serializer.validated_data.items():
            if key == "username":
                username_exists = User.objects.filter(username__iexact=value).first()
                if username_exists:
                    return Response(
                        {"error": "username already taken."}, status.HTTP_400_OK
                    )

            if key == "email":
                email_exists = User.objects.filter(username__iexact=value).first()
                if email_exists:
                    return Response(
                        {"error": "email already registered."}, status.HTTP_400_OK
                    )
            if key == "password":
                user.set_password(value)
            else:
                setattr(user, key, value)
        user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer
