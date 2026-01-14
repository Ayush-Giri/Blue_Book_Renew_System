from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_profile.models import UserProfile

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """
     Serializers main job is to send backend data to front.
     Backend data can be in any specific format and front end may not understand that
     so main job of serializer is to convert backend data to JSON and send it via api to the front end
     so that front end can understand

     write_only=True on the password field ensures the raw password is not included in the serialized
     output (like JSON responses) when returning the user object.

     this serializers takes json object and convert it to python object to stores the database and
      there we returned user which we can tap into and fetch the object attributes and send it to front
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone_number', 'is_collector', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            is_collector=validated_data['is_collector'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        full_name = user.first_name + " " + user.last_name
        UserProfile.objects.create(user=user, name=full_name, member_since=user.date_joined)
        return user


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["password"])
        user.save(update_fields=["password"])
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("image", "address", "name")

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["role"] = user.is_collector

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        if not user.is_active:
            raise serializers.ValidationError(
                "This account has been disabled. Please contact admin."
            )

        if user.is_superuser == True:
            data["user"] = {
                "username": user.username,
                "phone_number": user.phone_number,
                "role": "admin"
            }
            return data

        elif user.is_collector == True:
            data["user"] = {
                "username": user.username,
                "phone_number": user.phone_number,
                "role": "collector"
            }
            return data

        else:
            data["user"] = {
                "username": user.username,
                "phone_number": user.phone_number,
                "role": "user"
            }
            return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",
                  "username",
                  "email",
                  "phone_number",
                  "is_active",
                  "is_superuser",
                  "is_collector",
                  "date_joined",
                  )


class UserActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("is_active",)



