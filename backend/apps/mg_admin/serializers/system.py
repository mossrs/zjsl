from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import Permission, ContentType, Group
from apps.userapp.models import Users


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class ContentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['id', 'name']


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class AdminSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    # 重写创建管理员方法 因为密码和is_staff
    def create(self, validated_data):
        validated_data['is_staff'] = True
        admin = super(AdminSerializer, self).create(validated_data)
        admin.set_password(validated_data['password'])
        admin.save()
        return admin

    # 修改管理员用户信息
    def update(self, instance, validated_data):
        admin = super(AdminSerializer, self).update(instance, validated_data)
        admin.set_password(validated_data.get('password', instance.password))
        admin.save()
        return admin
