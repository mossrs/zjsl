from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from apps.mg_admin.utils import *
from apps.mg_admin.serializers.user import *
from apps.userapp.models import Users
from rest_framework.permissions import IsAdminUser


class UsersViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    pagination_class = PageNumPagination
    queryset = Users.objects.order_by('-id')
    # serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username', 'id', 'phone', 'email']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserAddSerializer

    # def get_queryset(self):
    #     q_search = self.request.query_params.get('search')
    #     if q_search == '' or q_search is None:
    #         return Users.objects.order_by('-id')
    #     else:
    #         return Users.objects.filter(username=q_search).order_by('-id')

