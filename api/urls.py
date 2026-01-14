from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("admin/users/", views.UserReadView.as_view()),
    path("admin/users/<int:user_id>/active-status/", views.UserReadView.as_view()),
    # path("admin/users/active-status", views.ToggleUserStatusView.as_view())
]

