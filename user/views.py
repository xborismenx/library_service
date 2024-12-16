from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserProfileSerializer, UserCreateSerializer


@extend_schema(
    summary="Creates a user's profile",
)
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Retrieves a user's profile",
    ),
    put=extend_schema(
        summary="Updates a user's profile"),
    patch=extend_schema(
        summary="Updates a user's profile",
    )
)
class MeApiView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
