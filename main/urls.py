from django.urls import path
from . import views

urlpatterns = [
    path('', views.adduser),
    path('api/users/', views.GetCapitalInfoView.as_view()),
]