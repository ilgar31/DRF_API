from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User


from .models import Profile
from .serializers import ProfileSerializer
from .forms import UserRegistrationForm


class GetCapitalInfoView(APIView):
    def get(self, request):
        queryset = Profile.objects.all()
        serializer_for_queryset = ProfileSerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer_for_queryset.data)


def adduser(requests):
    user_form = UserRegistrationForm({'email': 'test@gmail.com', 'password': '1234567890'})
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.is_active = False
        new_user.save()
    return
