from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.mg_admin.utils import PageNumPagination
from django.contrib.auth.models import Permission, ContentType, Group
from apps.userapp.models import Users
from ..serializers.system import PermissionSerializer, ContentTypeSerializer, GroupSerializer, AdminSerializer


class PermissionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    pagination_class = PageNumPagination
    queryset = Permission.objects.order_by('-id')
    serializer_class = PermissionSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name', 'codename']

    @action(methods=['get'], detail=False)
    def content_types(self, request):
        queryset = ContentType.objects.order_by('id')
        ser = ContentTypeSerializer(queryset, many=True)
        return Response(ser.data)


class GroupViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    pagination_class = PageNumPagination
    queryset = Group.objects.order_by('-id')
    serializer_class = GroupSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']


class AdminViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    pagination_class = PageNumPagination
    queryset = Users.objects.filter(is_staff=True).order_by('-id')
    serializer_class = AdminSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'username', 'phone', 'email']


