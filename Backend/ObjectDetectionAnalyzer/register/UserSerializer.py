from rest_framework import serializers
from rest_framework.authtoken.admin import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for data from RegisterView
    """

    class Meta:
        model = User
        fields = ['username', 'email']
