from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    email = serializers.CharField(source="username", max_length=200)
    name = serializers.CharField(source='profile.name', max_length=200)
    balance = serializers.IntegerField(source='profile.balance')
    status = serializers.IntegerField(source='profile.status')
