from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .views import (
    UserDetailView,
    UserSignupView
)

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("detail", UserDetailView.as_view(), name="user_detail"),
    path("detail/<int:pk>", UserDetailView.as_view(), name="other_user_detail"),
    path("signup", UserSignupView.as_view(), name="user_signup")
]
