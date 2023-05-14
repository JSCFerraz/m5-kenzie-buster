from rest_framework_simplejwt import views
from django.urls import path
from .views import UserView, UserDetailView
from .views import LoginJWTView


urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<int:user_id>/", UserDetailView.as_view()),
    path("users/login/", LoginJWTView.as_view()),
    path("users/login/refresh/", views.TokenRefreshView.as_view()),
]
