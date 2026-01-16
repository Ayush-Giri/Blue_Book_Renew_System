from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'vehicles', views.UserVehicleViewSet, basename='user-vehicle')

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', views.SignupView.as_view()),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("admin/users/", views.UserReadView.as_view()),
    path('admin/all-vehicles/', views.AdminAllVehiclesListView.as_view(), name='admin-all-vehicles'),
    path("admin/users/<int:user_id>/active-status/", views.UserReadView.as_view()),
    path("vehicle-types/", views.VehicleTypeView.as_view(), name="vehicle-types"),
    path("vehicle-ownerships/", views.VehicleOwnershipView.as_view(), name="vehicle-ownerships"),
    path("vehicle-fuel-types/", views.VehicleFuelTypeView.as_view(), name="vehicle-fuel-types"),
    path("vehicle-engine-capacities/", views.VehicleEngineCapacityView.as_view(), name="vehicle-engine-capacities"),

    # path("admin/users/active-status", views.ToggleUserStatusView.as_view())
]

