from rest_framework.status import HTTP_204_NO_CONTENT

from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission, SAFE_METHODS


from users.models import User, Address
from users.api.serializers import *


class IsSafeMethodAndAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and
            request.user.is_authenticated or
            request.user and request.user.is_staff
        )


class UserAPIView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSafeMethodAndAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, id_slug=pk)
        serializer = self.get_serializer(user)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, id_slug=pk)
        user.delete()

        return Response({"message": "user deleted"})


class AddressAPIView(ModelViewSet):
    def get(self, request):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
