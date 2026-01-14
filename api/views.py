from api.serializers import SignupSerializer
from django.contrib.auth import get_user_model
from api.permissions import IsAdmin
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from user_profile.models import UserProfile
from api.serializers import ProfileSerializer, PasswordSerializer, UserReadSerializer
from api.permissions import IsActiveUser
from api.serializers import UserActiveSerializer



# Create your views here.


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # when we return Response object from serializer views we are essentially returning json
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# class ToggleUserStatusView(APIView):
#     permission_classes = [IsAuthenticated, IsAdmin]
#
#     def patch(self, request, user_id):
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response(
#                 {"error": "User not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#
#         # prevent admin disabling himself
#         if user == request.user:
#             return Response(
#                 {"error": "You cannot disable yourself"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         serializer = UserActiveSerializer(
#             user,
#             data=request.data,
#             partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(
#             {
#                 "user_id": user.id,
#                 "is_active": user.is_active
#             },
#             status=status.HTTP_200_OK
#         )

