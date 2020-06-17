from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the users object """

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        """ Create new user with encrypted password and return it """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ Updating user and ensure password is set correctly """
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        user.set_password(password)
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user authentication object """

    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """ Validating and authenticaing the user """
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            message = _("Email/Password is incorrect")
            raise serializers.ValidationError(message, code="authentication")
        attrs["user"] = user
        return attrs
