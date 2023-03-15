from rest_framework import serializers
from apps.userapp.models import Users


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['id', 'username', 'phone', 'email']


class UserAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'phone', 'email', 'password']
        extra_kwargs = {
            'username': {
                'max_length': 8,
                'min_length': 5,
            },
            'password': {
                'max_length': 8,
                'min_length': 3,
                'write_only': True,  # 只能写入数据库不能显示在页面中
            },

        }

    def create(self, validated_data):
        # 新增用户数据
        user = Users.objects.create_user(**validated_data)
        return user
