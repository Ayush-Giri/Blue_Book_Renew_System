from rest_framework import serializers
from . import models


class SignupSerializer(serializers.ModelSerializer):
    """
     Serializers main job is to send backend data to front.
     Backend data can be in any specific format and front end may not understand that
     so main job of serializer is to convert backend data to JSON and send it via api to the front end
     so that front end can understand

     write_only=True on the password field ensures the raw password is not included in the serialized
     output (like JSON responses) when returning the user object.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ('username', 'email', 'password', 'phone_number', 'is_collector')

    def create(self, validated_data):
        user = models.User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['phone_number'],
            is_collector=validated_data['is_collector']


        )
        return user
