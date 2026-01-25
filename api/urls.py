from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'vehicles', views.UserVehicleViewSet, basename='user-vehicle')

urlpatterns = [
    path('', include(router.urls)),
    path("taxes/", views.VehicleTaxPostView.as_view()),
    path("taxes/all-taxes/", views.VehicleTaxAllGetView.as_view()),
    path("taxes/<int:user_vehicle_id>/", views.VehicleTaxView.as_view()),
    path("all-collectors/", views.AllCollectorView.as_view()),
    path('collector-view/user_id/', views.CollectorView.as_view()),
    path('collection-center/', views.CollectionCenterView.as_view()),
    path('collection-center/collector/<int:user_id>/', views.CollectionCenterSingleView.as_view()),
    path('collection-center/<int:user_id>/', views.CollectionCenterPostPatchView.as_view()),
    path('renew-requests/', views.RenewRequestView.as_view(), name='renew-request-list'),
    path('renew-requests/<int:id>/', views.RenewRequestView.as_view(), name='renew-request-detail'),
    path("service-charge/", views.ServiceChargeView.as_view()),
    path("service-charge/<int:id>/", views.ServiceChargePatchView.as_view()),
    path("insurance/", views.InsuranceView.as_view()),
    path("insurance/<int:id>/", views.InsurancePatchView.as_view()),
    path('signup/', views.SignupView.as_view()),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/<int:id>/", views.AdminProfileEdit.as_view()),
    path("collector-profile/<int:user_id>/", views.CollectorView.as_view()),
    path("admin/users/", views.UserReadView.as_view()),
    path('admin/all-vehicles/', views.AdminAllVehiclesListView.as_view(), name='admin-all-vehicles'),
    path("admin/users/<int:user_id>/active-status/", views.UserReadView.as_view()),
    path("vehicle-types/", views.VehicleTypeView.as_view(), name="vehicle-types"),
    path("vehicle-ownerships/", views.VehicleOwnershipView.as_view(), name="vehicle-ownerships"),
    path("vehicle-fuel-types/", views.VehicleFuelTypeView.as_view(), name="vehicle-fuel-types"),
    path("vehicle-engine-capacities/", views.VehicleEngineCapacityView.as_view(), name="vehicle-engine-capacities"),
    # path("admin/users/active-status", views.ToggleUserStatusView.as_view())
]

