from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """

    Args:
        serializers (Serializer): Serializer class for User model
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

    def create(self, validated_data: dict):
        # not adding any particular checking right now, the serializer will throw an error
        # if the above fields are not provided in the post request to /users
        return super().create(validated_data)

    def delete(self, instance: User):
        instance.delete()


class UserAuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs: dict):
        """Validates the incoming login data/request.

        Args:
            attrs (dictionary): the attributes being sent to verify login, an email and password string

        Returns:
            _type_: _description_
        """

        email = attrs.get("email", None)
        password = attrs.get("password", None)

        if (email is not None and email != "") and (
            password is not None and password != ""
        ):
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = "Must include 'email' and 'password'."
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        # not adding any particular checking right now, the serializer will throw an error
        # if the above fields are not provided in the post request to /users
        if validated_data.get("is_superuser", False) is False:
            User.objects.create_user(**validated_data)

        else:
            pass

        return super().create(validated_data)
