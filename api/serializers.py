from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_profile.models import UserProfile
# from vehicles import models as user_vehicle_models
from vehicles.models import UserVehicle, VehicleType, VehicleFuelType, VehicleOwnership
from collector.models import CollectorModel

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
        fields = ("user", "image", "address", "name")

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
                  "first_name",
                  "last_name",
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


from rest_framework import serializers
from vehicles import models as user_vehicles_models


# --- Helper Serializers for Nested Objects ---
class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_vehicles_models.VehicleType
        fields = ['id', 'name']


class VehicleFuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_vehicles_models.VehicleFuelType
        fields = ['id', 'name']


class VehicleOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_vehicles_models.VehicleOwnership
        fields = ['id', 'name']


class VehicleCapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = user_vehicles_models.VehicleCapacity
        fields = ("id", "capacity_value")


# --- Main Vehicle Serializer ---
class UserVehicleSerializer(serializers.ModelSerializer):
    # Display objects for GET requests
    vehicle_type_detail = VehicleTypeSerializer(source='vehicle_type', read_only=True)
    fuel_type_detail = VehicleFuelTypeSerializer(source='fuel_type', read_only=True)
    ownership_type_detail = VehicleOwnershipSerializer(source='ownership_type', read_only=True)
    engine_capacity_detail = VehicleCapacitySerializer(source='engine_capacity', read_only=True)

    # Read-only fields
    user = serializers.ReadOnlyField(source='user.username')
    current_tax_amount = serializers.ReadOnlyField()
    expiry_date = serializers.ReadOnlyField()

    class Meta:
        model = user_vehicles_models.UserVehicle
        # fields = [
        #     'id', 'user', 'brand_and_model', 'color', 'chassis_number',
        #     'engine_number', 'issue_date', 'expiry_date', 'vehicle_number' 'engine_capacity',
        #     'current_tax_amount',
        #     'vehicle_type', 'ownership_type', 'fuel_type',  # Used for POST (IDs)
        #     'vehicle_type_detail', 'ownership_type_detail', 'fuel_type_detail'  # Used for GET (Objects)
        # ]
        fields = "__all__"
        # Hide the ID fields from GET response to keep it clean, but allow them for POST
        extra_kwargs = {
            'vehicle_type': {'write_only': True},
            'ownership_type': {'write_only': True},
            'fuel_type': {'write_only': True},
            'engine_capacity': {'write_only': True},
        }


# class VehicleTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = user_vehicles_models.VehicleType
#         fields = ("name", )


class VehicleOwnerShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_vehicles_models.VehicleOwnership
        fields = ("id", "name",)


#
# class VehicleFuelTypeSerializer(serializers.ModelSerializer):
#     # This tells DRF: We are working with a Django model
#     # VehicleFuelType table in the database
#     # Only
#     # the
#     # name
#     # field is exposed
#     # Serializer
#     # will:
#     #
#     # ✅ Read
#     # only
#     # name
#     # from the model
#     #
#     # ✅ Accept
#     # only
#     # name
#     # from incoming JSON
#     class Meta:
#         model = user_vehicles_models.VehicleFuelType
#         fields = ("name", )


class VehicleEngineCapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = user_vehicles_models.VehicleCapacity
        fields = ("id", "capacity_value",)


class AdminGetAllVehiclesSerializer(serializers.ModelSerializer):
    # Nesting the user details so Admin knows who owns what
    user_details = serializers.SerializerMethodField()

    # Human-readable details for the dropdown fields
    vehicle_type_name = serializers.ReadOnlyField(source='vehicle_type.name')
    fuel_type_name = serializers.ReadOnlyField(source='fuel_type.name')
    ownership_type_name = serializers.ReadOnlyField(source='ownership_type.name')
    capacity_value = serializers.ReadOnlyField(source='engine_capacity.capacity_value')

    class Meta:
        model = user_vehicles_models.UserVehicle
        fields = (
            'id', 'user_details', 'brand_and_model', 'vehicle_number',
            'chassis_number', 'engine_number', 'color', 'issue_date',
            'expiry_date', 'current_tax_amount', 'vehicle_type_name',
            'fuel_type_name', 'ownership_type_name', 'capacity_value'
        )

    def get_user_details(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "phone": obj.user.phone_number,
            "email": obj.user.email
        }


class CollectorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectorModel
        fields = ("collection_center_name", "collection_center_address", "collection_center_number")


