from django.urls import path
from . import views

urlpatterns = [
    #read
    path('get/all/', views.GetAllInfoView.as_view()),
    path('get/user/<str:email>/', views.GetUserInfoView.as_view()),
    path('get/user_departments/<str:email>/', views.GetUserDepartmentsView.as_view()),
    path('get/user_employees/<str:email>/', views.GetUserEmployeesView.as_view()),
    path('get/user_markups/<str:email>/', views.GetUserMarkupsView.as_view()),
    path('get/user_products/<str:email>/', views.GetUserProductsView.as_view()),
    path('get/user_sales/<str:email>/', views.GetUserSalesView.as_view()),
    path('get/user_returns/<str:email>/', views.GetUserReturnsView.as_view()),
    #add
    path('add/user/<str:data>/', views.AddUserView.as_view()),
]