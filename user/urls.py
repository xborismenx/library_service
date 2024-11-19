from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import MeApiView, UserCreateAPIView

app_name = "user"

urlpatterns = [
    path("", UserCreateAPIView.as_view(), name="create-user"),
    path("me/", MeApiView.as_view(), name="me"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

