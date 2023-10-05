from rest_framework import generics
from .serializers import (
    UserAuthenticationSerializer,
    UserSignupSerializer,
    UserSerializer,
)
from .models import User
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

# Create your views here.


class UsersView(generics.ListCreateAPIView):
    """View for returning a list of all the users in the application.

    This view can be used to create users for signup via the UserSerializers create method.

    Args:
        generics (generics): Generic view for returning a list of all the users in the application.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserLoginView(ObtainAuthToken):
    """View for logging in a user.

    Args:
        ObtainAuthToken (ObtainAuthToken): Class for obtaining the token, modifies the permissions to allow any user to login.
        The token provided can be used as basic authorization scheme, in POSTMAN you can use this as OAuth 2.0 Bearer Token.
        Within the front end, this will need to be passed through the header as AUTHORIZATION: TOKEN <token>.

    Returns:
        Response: Returns a response with the token and user id.
    """

    serializer_class = UserAuthenticationSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = UserAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])

        return Response(
            {"Token": f"{token.key}", "UserId": f"{token.user_id}"},
            status=status.HTTP_200_OK,
        )


class UserSignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        required = ["username", "email", "password", "first_name", "last_name"]
        try:
            if not all([field in request.data for field in required]):
                raise Exception(
                    f"Missing required one of the required fields: {required}"
                )

            user_data = request.data
            user = User.objects.create_user(**user_data)
            serialized = UserSerializer(user).data
        except Exception as e:
            return Response(
                {"error": "Error creating user.", "message": f"{e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "User created successfully", "user": serialized}, status=status.HTTP_201_CREATED)
