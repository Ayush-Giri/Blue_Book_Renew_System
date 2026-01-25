from api.serializers import SignupSerializer
from django.contrib.auth import get_user_model
from user_profile.models import UserProfile
from api.serializers import ProfileSerializer, PasswordSerializer, UserReadSerializer
from api.permissions import IsActiveUser
from api.serializers import UserActiveSerializer
from rest_framework import viewsets, permissions
from vehicles import models as user_vehicles_models
from .serializers import UserVehicleSerializer
from vehicles.models import VehicleType, VehicleOwnership, VehicleFuelType, VehicleCapacity
from .serializers import VehicleTypeSerializer, VehicleOwnerShipSerializer, VehicleFuelTypeSerializer, \
    VehicleEngineCapacitySerializer
from rest_framework import generics, filters
from .permissions import IsAdmin, IsAdminOrReadOnly  # Assuming you have this custom permission
from api.serializers import AdminGetAllVehiclesSerializer
from api.serializers import CollectorModelSerializer
from collector.models import CollectorModel
from api.serializers import InsuranceModelSerializer
from insurance.models import InsuranceModel
from service_charge.models import ServiceChargeModel
from api.serializers import ServiceChargeSerializer
from renew_request.models import RenewRequest
from api.serializers import RenewRequestSerializer
from api.serializers import CollectionCenterSerializer
from collector.models import CollectionCenterModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from api.serializers import GetAllCollectorSerializer
# from api.serializers import VehicleTaxSerializer
from vehicles.models import VehicleTax
from api.serializers import VehicleTaxSerializer
from vehicles.models import UserVehicle


# Create your views here.

class VehicleTypeView(APIView):
    def get(self, request):
        vehicle_types = VehicleType.objects.all()
        serializer = VehicleTypeSerializer(vehicle_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VehicleTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VehicleOwnershipView(APIView):
    def get(self, request):
        ownership_types = VehicleOwnership.objects.all()
        serializer = VehicleOwnerShipSerializer(ownership_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VehicleOwnerShipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VehicleFuelTypeView(APIView):
    def get(self, request):
        fuel_type = VehicleFuelType.objects.all()
        serializer = VehicleFuelTypeSerializer(fuel_type, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VehicleFuelTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VehicleEngineCapacityView(APIView):
    def get(self, request):
        engine_capacity = VehicleCapacity.objects.all()
        serializer = VehicleEngineCapacitySerializer(engine_capacity, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VehicleEngineCapacitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.save().id
            # when we return Response object from serializer views we are essentially returning json
            return Response(
                {"message": "User created successfully",
                 "id": user_id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AdminProfileEdit(APIView):
#     permission_classes = [IsAuthenticated, IsAdmin]
#
#     def patch(self, request, id):
#         try:
#             user = UserProfile.objects.get(user_id=id)
#             serializer = ProfileSerializer(user, data=request.data, partial=True)
#             print(request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(
#                     {"message": "updated successfully"},
#                     status=status.HTTP_200_OK
#                 )
#             return Response(
#                 {"message": "invalid format"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         except UserProfile.DoesNotExist:
#             return Response(
#                 {"message": "User does not exist"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

# class AdminProfileEdit(APIView):
#     permission_classes = [IsAuthenticated, IsAdmin]
#
#     def patch(self, request, id):
#         try:
#             # Look up by user_id
#             profile = UserProfile.objects.get(user_id=id)
#
#             # Pass the profile instance and the data
#             serializer = ProfileSerializer(profile, data=request.data, partial=True)
#
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(
#                     {
#                         "message": "updated successfully",
#                         "data": serializer.data  # Return data to verify the change
#                     },
#                     status=status.HTTP_200_OK
#                 )
#
#             # This will tell you EXACTLY what is wrong with your JSON
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         except UserProfile.DoesNotExist:
#             return Response(
#                 {"message": "User Profile for this ID does not exist"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

# class AdminProfileEdit(APIView):
#     permission_classes = [IsAuthenticated, IsAdmin]
#
#     def patch(self, request, id):
#         try:
#             # 1. Get the Profile
#             profile = UserProfile.objects.get(user_id=id)
#             user = profile.user  # Access the linked User model
#
#             # 2. Update User-level fields if they are in the request
#             # This ensures first_name and last_name change in the main User table
#             if 'first_name' in request.data:
#                 user.first_name = request.data['first_name']
#             if 'last_name' in request.data:
#                 user.last_name = request.data['last_name']
#
#             user.save()
#
#             # 3. Update Profile-level fields (like address, image, and the combined name)
#             serializer = ProfileSerializer(profile, data=request.data, partial=True)
#
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({
#                     "message": "updated successfully",
#                     "data": serializer.data
#                 }, status=status.HTTP_200_OK)
#
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         except UserProfile.DoesNotExist:
#             return Response({"message": "User does not exist"}, status=404)


class AdminProfileEdit(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, id):
        try:
            # 1. Fetch the UserProfile using the user_id from the URL
            profile = UserProfile.objects.get(user_id=id)
            user = profile.user  # This is the User object where phone_number lives

            # 2. Check if phone_number is in the request and update the User table
            phone_number = request.data.get('phone_number')
            if phone_number:
                user.phone_number = phone_number
                user.save(update_fields=['phone_number'])

            # 3. Update the Profile fields (name, address, image)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()

                # We construct a custom response so you can see both updates
                return Response({
                    "message": "User and Profile updated successfully",
                    "data": {
                        "phone_number": user.phone_number,
                        "name": profile.name,
                        "address": profile.address,
                        "image": serializer.data.get('image')
                    }
                }, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except UserProfile.DoesNotExist:
            return Response({"message": "User profile not found"}, status=404)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated, IsActiveUser]

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                "name": request.user.get_full_name() or request.user.username,
                "member_since": request.user.date_joined.date(),
            }
        )

        image_url = (
            request.build_absolute_uri(profile.image.url)
            if profile.image
            else None
        )

        return Response(
            {
                "id": request.user.id,
                "name": profile.name,
                "email": request.user.email,
                "phone_number": request.user.phone_number,
                "address": profile.address,
                "image": image_url,
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request):
        user = request.user

        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "name": user.get_full_name() or user.username,
                "member_since": user.date_joined.date(),
            }
        )

        # 🔹 1. Update PROFILE fields
        profile_data = {
            key: value
            for key, value in request.data.items()
            if key in ["image", "address", "name"]
        }

        if profile_data:
            profile_serializer = ProfileSerializer(
                profile,
                data=profile_data,
                partial=True,
                context={"request": request}
            )
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        # 🔹 2. Update USER fields
        phone_number = request.data.get("phone_number")
        if phone_number is not None:
            user.phone_number = phone_number
            user.save(update_fields=["phone_number"])

        email = request.data.get("email")
        if email is not None:
            user.email = email
            user.save(update_fields=["email"])
        if "old_password" in request.data and "password" in request.data:
            password_serializer = PasswordSerializer(
                data={
                    "old_password": request.data.get("old_password"),
                    "password": request.data.get("password"),
                },
                context={"request": request}
            )
            password_serializer.is_valid(raise_exception=True)
            password_serializer.save()

        return Response(
            {"message": "Profile updated successfully"},
            status=status.HTTP_200_OK
        )


User = get_user_model()


class ToggleUserStatusView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Prevent admin disabling himself
        if user == request.user:
            return Response(
                {"error": "You cannot disable yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_active = not user.is_active
        user.save(update_fields=["is_active"])

        return Response(
            {
                "message": f"User {'enabled' if user.is_active else 'disabled'} successfully",
                "user_id": user.id,
                "is_active": user.is_active
            },
            status=status.HTTP_200_OK
        )


class UserReadView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all()

        serializer = UserReadSerializer(users, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # prevent admin disabling himself
        if user == request.user:
            return Response(
                {"error": "You cannot disable yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserActiveSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "user_id": user.id,
                "is_active": user.is_active
            },
            status=status.HTTP_200_OK
        )


class UserVehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for User Vehicles.
    GET: Returns owned vehicles with nested type objects.
    POST: Creates vehicle (Calculates Tax & Expiry).
    PATCH: Updates specific fields.
    """
    serializer_class = UserVehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Debugging info in terminal
        print(f"\n--- API Request by: {user.username} ---")

        # Admins/Collectors see all; Users see only theirs
        if user.is_staff or getattr(user, 'is_collector', False):
            return user_vehicles_models.UserVehicle.objects.all()

        return user_vehicles_models.UserVehicle.objects.filter(user=user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user to the vehicle
        serializer.save(user=self.request.user)


class AdminAllVehiclesListView(generics.ListAPIView):
    """
    Returns a list of ALL vehicles registered in the system.
    Only accessible by Admin/Superusers.
    """
    queryset = user_vehicles_models.UserVehicle.objects.all().select_related(
        'user', 'vehicle_type', 'fuel_type', 'ownership_type', 'engine_capacity'
    )
    serializer_class = AdminGetAllVehiclesSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    # Adding Search & Filter (Crucial for Admin real-world projects)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['vehicle_number', 'chassis_number', 'user__username', 'user__phone_number']
    ordering_fields = ['issue_date', 'current_tax_amount']


class CollectorView(APIView):
    # permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, user_id):
        try:
            collector = CollectorModel.objects.get(user_id=user_id)
            serializer = CollectorModelSerializer(collector)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except CollectorModel.DoesNotExist:
            return Response(
                {"message": "collector profile does not exist for this user"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Step 3: If it's NOT a "DoesNotExist" error, tell us what it actually is!
            return Response(
                {"error": "Serializer or Server Error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.is_collector:
            serializer = CollectorModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(
                    {"message": "collector successfully created"},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "user is not a collector"},
                status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, user_id):
        try:
            collector_profile = CollectorModel.objects.get(user_id=user_id)
            serializer = CollectorModelSerializer(collector_profile, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "updated successfully", "data": serializer.data},
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    "error": "collector profile not found",

                },
                status=status.HTTP_404_NOT_FOUND
            )
        except CollectorModel.DoesNotExist:
            return Response(
                {"error": "Collector profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )


# class CollectionCenterView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         # Fetch all centers
#         centers = CollectionCenterModel.objects.all()
#         # many=True is required when serializing a list of objects
#         serializer = CollectionCenterSerializer(centers, many=True)
#         return Response(
#             {
#                 "message": "fetched successfully",
#                 "data": serializer.data  # You must include the data here
#             },
#             status=status.HTTP_200_OK
#         )
#
#     def post(self, request):
#         # Check if collector profile already exists to prevent duplicates
#         if CollectorModel.objects.filter(user=request.user).exists():
#             return Response({"message": "You already manage a center"}, status=status.HTTP_400_BAD_REQUEST)
#
#         if request.user.is_staff or request.user.is_collector:
#             serializer = CollectionCenterSerializer(data=request.data)
#             if serializer.is_valid():
#                 center_instance = serializer.save()
#                 CollectorModel.objects.create(
#                     user=request.user,
#                     collection_center=center_instance
#                 )
#                 return Response({"message": "created successfully"}, status=status.HTTP_201_CREATED)
#
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         return Response({"message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
#
#     def patch(self, request):
#         try:
#             # 1. Get the Collector profile for the logged-in user
#             collector_profile = request.user.collector_profile
#             # 2. Get the specific center linked to this collector
#             center_instance = collector_profile.collection_center
#         except CollectorModel.DoesNotExist:
#             return Response({"message": "No center found for this user"}, status=status.HTTP_404_NOT_FOUND)
#
#         # 3. Pass the center instance (not the user) to the serializer
#         serializer = CollectionCenterSerializer(center_instance, data=request.data, partial=True)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionCenterView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            collection_centers = CollectionCenterModel.objects.all()
            serializer = CollectionCenterSerializer(collection_centers, many=True)
            return Response(
                {"message": "fetched successfully",
                 "data": serializer.data},
                status=status.HTTP_200_OK
            )
        except CollectionCenterModel.DoesNotExist:
            return Response(
                {"message": "no collection center exist"},
                status=status.HTTP_400_BAD_REQUEST
            )


# class CollectionCenterSingleView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, collector_id):
#         # 1. Fetch the collector using its own Primary Key (ID)
#         # If ID 47 is passed, it looks for Collector #47
#         collector = get_object_or_404(CollectorModel, id=collector_id)
#
#         # 2. Check if this collector actually has a center assigned
#         if not collector.collection_center:
#             return Response(
#                 {"error": "This collector does not have an assigned collection center."},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#
#         # 3. Serialize and return the center data
#         serializer = CollectionCenterSerializer(collector.collection_center)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class CollectionCenterSingleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id): # Renamed variable to user_id for clarity
        # 1. Find the Collector profile that belongs to User #52
        collector = get_object_or_404(CollectorModel, user_id=user_id)

        # 2. Check if this collector has an assigned center
        if not collector.collection_center:
            return Response(
                {"error": "This collector has no assigned collection center."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3. Serialize the center linked to that collector
        serializer = CollectionCenterSerializer(collector.collection_center)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CollectionCenterPostPatchView(APIView):
    # Change collector_id to user_id to match the User Table ID
    def post(self, request, user_id):
        # 1. Look for the collector profile using the USER's ID
        collector = get_object_or_404(CollectorModel, user_id=user_id)

        if not (request.user.is_staff or request.user == collector.user):
            return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        if collector.collection_center:
            return Response({"message": "Collector already has a center. Use PATCH."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = CollectionCenterSerializer(data=request.data)
        if serializer.is_valid():
            center_instance = serializer.save()
            collector.collection_center = center_instance
            collector.save()
            return Response({"message": "Created and assigned successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id):
        # Look for the profile using user_id
        collector = get_object_or_404(CollectorModel, user_id=user_id)

        if not (request.user.is_staff or request.user == collector.user):
            return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        center_instance = collector.collection_center
        if not center_instance:
            return Response({"message": "No center found to update."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionCenterSerializer(center_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class  CollectionCenterPostPatchView(APIView):
#
#     def post(self, request, collector_id):
#         # 1. Fetch the specific collector
#         collector = get_object_or_404(CollectorModel, id=collector_id)
#
#         # 2. Check Permissions (Staff or the collector themselves)
#         if not (request.user.is_staff or request.user == collector.user):
#             return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
#
#         # 3. Check if collector already has a center
#         if collector.collection_center:
#             return Response({"message": "Collector already has a center. Use PATCH to update."},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = CollectionCenterSerializer(data=request.data)
#         if serializer.is_valid():
#             # Create center and link to the specific collector
#             center_instance = serializer.save()
#             collector.collection_center = center_instance
#             collector.save()
#
#             return Response({"message": "Created and assigned successfully"}, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, collector_id):
#         # 1. Fetch the specific collector
#         collector = get_object_or_404(CollectorModel, id=collector_id)
#
#         # 2. Check Permissions
#         if not (request.user.is_staff or request.user == collector.user):
#             return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
#
#         # 3. Get the center associated with this collector
#         center_instance = collector.collection_center
#         if not center_instance:
#             return Response({"message": "No center found for this collector to update."},
#                             status=status.HTTP_404_NOT_FOUND)
#
#         # 4. Update the center instance
#         serializer = CollectionCenterSerializer(center_instance, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CollectionCenterPostPatchView(APIView):
#
# def post(self, r):
# class CollectionCenterPostPatchView(APIView):
#
#     def post(self, request, collector_id):
#         # 1. Fetch the specific collector
#         collector = get_object_or_404(CollectorModel, id=collector_id)
#
#         # 2. Check Permissions (Staff or the collector themselves)
#         if not (request.user.is_staff or request.user == collector.user):
#             return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
#
#         # 3. Check if collector already has a center
#         if collector.collection_center:
#             return Response({"message": "Collector already has a center. Use PATCH to update."},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = CollectionCenterSerializer(data=request.data)
#         if serializer.is_valid():
#             # Create center and link to the specific collector
#             center_instance = serializer.save()
#             collector.collection_center = center_instance
#             collector.save()
#
#             return Response({"message": "Created and assigned successfully"}, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, collector_id):
#         # 1. Fetch the specific collector
#         collector = get_object_or_404(CollectorModel, id=collector_id)
#
#         # 2. Check Permissions
#         if not (request.user.is_staff or request.user == collector.user):
#             return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
#
#         # 3. Get the center associated with this collector
#         center_instance = collector.collection_center
#         if not center_instance:
#             return Response({"message": "No center found for this collector to update."},
#                             status=status.HTTP_404_NOT_FOUND)
#
#         # 4. Update the center instance
#         serializer = CollectionCenterSerializer(center_instance, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # def post(self, request, collector_id):
#     if request.user.is_staff or request.user.is_collector:
#         serializer = CollectionCenterSerializer(data=request.data)
#         if serializer.is_valid():
#             collection_center_instance = serializer.save()
#             CollectorModel.objects.create(
#                 id=collecto
#                 collection_center=collection_center_instance
#             )
#             return Response(
#                 {"message": "created successfully"},
#                 status=status.HTTP_200_OK
#             )
#
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )
#     return Response(
#         {"message": "only admin and collector can add collection center"},
#         status=status.HTTP_403_FORBIDDEN
#     )
#
# def patch(self, request):
#     if request.user.is_staff and request.user.is_collector:
#         serializer = CollectionCenterSerializer(request.user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "updated successfully"},
#                 status=status.HTTP_200_OK
#             )
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )
#     return Response(
#         {"message": "only admin and collector can update collection center"},
#         status=status.HTTP_400_BAD_REQUEST
#     )


class InsuranceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admins can add insurance providers"},
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            serializer = InsuranceModelSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Insurance Provider added successfully"},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request):
        all_insurance_providers = InsuranceModel.objects.all()
        serializer = InsuranceModelSerializer(all_insurance_providers, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class InsurancePatchView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, id):
        try:
            insurance = InsuranceModel.objects.get(id=id)
            serializer = InsuranceModelSerializer(insurance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "updated successfully"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except InsuranceModel.DoesNotExist:
            return Response(
                {"message": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class ServiceChargeView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        all_service_charge = ServiceChargeModel.objects.get(id=1)
        serializer = ServiceChargeSerializer(all_service_charge)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        if len(ServiceChargeModel.objects.all()) >= 1:
            return Response(
                {"message": "cannot add more service charge"},
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            if request.user.is_staff:
                serializer = ServiceChargeSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"message": "Service Charge Created Successfully"},
                        status=status.HTTP_201_CREATED
                    )
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {"message": "invalid"},
                    status=status.HTTP_400_BAD_REQUEST
                )


class ServiceChargePatchView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        if request.user.is_staff:
            try:
                service_charge = ServiceChargeModel.objects.get(id=id)
                serializer = ServiceChargeSerializer(service_charge, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"message": "updated successfully"},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ServiceChargeModel.DoesNotExist:
                return Response(
                    {"message": "no such record for service charge"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"message": "only accessible to admin"},
                status=status.HTTP_403_FORBIDDEN
            )


class RenewRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Admins see all requests, Users only see their own
        if request.user.is_staff:
            queryset = RenewRequest.objects.all()
        else:
            queryset = RenewRequest.objects.filter(user=request.user)

        serializer = RenewRequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # When creating, we manually assign the logged-in user
        serializer = RenewRequestSerializer(data=request.data)

        if serializer.is_valid():
            # Security Check: Ensure the vehicle belongs to the person logged in
            vehicle = serializer.validated_data['vehicle']
            if vehicle.user != request.user:
                return Response(
                    {"detail": "You cannot request renewal for a vehicle you do not own."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Auto-fetch the latest service charge if not provided
            service_charge = ServiceChargeModel.objects.last()

            serializer.save(user=request.user, service_charge=service_charge)
            return Response(
                {"message": "Renew request submitted successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            renew_request = RenewRequest.objects.get(id=id)

            # Permission: Only Admins can change the status (Processing/Completed)
            # Users can only update their own requests if they are still 'pending'
            if not request.user.is_staff and renew_request.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = RenewRequestSerializer(
                renew_request,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Renew request updated successfully"},
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except RenewRequest.DoesNotExist:
            return Response(
                {"detail": "Request not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class AllCollectorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_collectors = CollectorModel.objects.all()
        serializer = GetAllCollectorSerializer(all_collectors, many=True)
        return Response(
            {"data": serializer.data},
            status=status.HTTP_200_OK
        )


class VehicleTaxPostView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.is_staff:
            serializer = VehicleTaxSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "vehicle tax added successfully"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"message": "invalid data", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message": "operation not allowed"},
            status=status.HTTP_403_FORBIDDEN
        )


class VehicleTaxAllGetView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def get(self, request):
        all_taxes = VehicleTax.objects.all()
        if len(all_taxes) == 0:
            return Response(
                {"message": "no taxes availabel"},
                status=status.HTTP_204_NO_CONTENT
            )
        serializer = VehicleTaxSerializer(all_taxes, many=True)
        return Response(
            {"message": "all taxes feteched successfully",
             "data": serializer.data,
             },
            status=status.HTTP_200_OK
        )


class VehicleTaxView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_vehicle_id):
        try:
            # 1. Get the specific vehicle owned by the user
            vehicle = UserVehicle.objects.get(id=user_vehicle_id)

            # 2. Use the calculate_tax logic we built in the model
            tax_amount = vehicle.calculate_tax()

            # 3. Find the actual Rule object to serialize it
            tax_rule = VehicleTax.objects.filter(
                vehicle_type=vehicle.vehicle_type,
                ownership_type=vehicle.ownership_type,
                fuel_type=vehicle.fuel_type,
                vehicle_capacity__capacity_value__gte=vehicle.engine_capacity.capacity_value
            ).order_by('vehicle_capacity__capacity_value').first()

            if not tax_rule:
                return Response({"message": "No tax rule found for this vehicle's specifications"}, status=404)

            serializer = VehicleTaxSerializer(tax_rule)
            return Response(
                {
                    "message": "Vehicle tax fetched successfully",
                    "data": serializer.data,
                    "calculated_amount": tax_amount  # Confirms the final price
                },
                status=status.HTTP_200_OK
            )
        except UserVehicle.DoesNotExist:
            return Response({"message": "Vehicle not found"}, status=404)



    def patch(self, request, user_vehicle_id):
        if request.user.is_staff:
            try:
                tax_rule = VehicleTax.objects.get(id=user_vehicle_id)
                serializer = VehicleTaxSerializer(tax_rule, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"message": "tax rule updated successfully"},
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {"message": "invalid", "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except VehicleTax.DoesNotExist:
                return Response(
                    {"message": "no such tax rule exists"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"message": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )





#
# class VehicleTaxView(APIView):
#     permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
#
#     def get(self, request):
#         taxes = VehicleTax.objects.select_related(
#             'vehicle_type', 'ownership_type', 'fuel_type', 'vehicle_capacity'
#         ).all()
#         serializer = VehicleTaxSerializer(taxes, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         # Only reached if IsAdminOrReadOnly passes (user.is_staff)
#         serializer = VehicleTaxSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk):
#         # Only reached if IsAdminOrReadOnly passes
#         try:
#             tax_rule = VehicleTax.objects.get(pk=pk)
#         except VehicleTax.DoesNotExist:
#             return Response({"error": "Tax rule not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = VehicleTaxSerializer(tax_rule, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

