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
    path('get/product_by_uid/<str:uid>/', views.GetProductView.as_view()),
    #add
    path('add/user/<str:data>/', views.AddUserView.as_view()),
    path('add/user_department/<str:data>/', views.AddUserDepartmentView.as_view()),
    path('add/user_employer/<str:data>/', views.AddUserEmployeesView.as_view()),
    path('add/user_markup/<str:data>/', views.AddUserMarkupView.as_view()),
    path('add/user_product/', views.AddUserProductView.as_view()),
    path('add/user_sale/', views.AddUserSaleView.as_view()),
    path('add/user_return/', views.AddUserReturnView.as_view()),
    #delete
    path('delete/user/<str:email>/', views.DeleteUserView.as_view()),
    path('delete/user_departments/<str:email>/', views.DeleteUserDepartmentsView.as_view()),
    path('delete/user_department/<str:data>/', views.DeleteUserDepartmentView.as_view()),
    path('delete/user_employees/<str:email>/', views.DeleteUserEmployeesView.as_view()),
    path('delete/user_employer/<str:data>/', views.DeleteUserEmployerView.as_view()),
    path('delete/user_markups/<str:email>/', views.DeleteUserMarkupsView.as_view()),
    path('delete/user_markup/<str:data>/', views.DeleteUserMarkupView.as_view()),
    path('delete/user_products/<str:email>/', views.DeleteUserProductsView.as_view()),
    path('delete/product/<str:uid>/', views.DeleteUserProductView.as_view()),
    path('delete/user_sales/<str:email>/', views.DeleteUserSalesView.as_view()),
    path('delete/user_sale/<str:data>/', views.DeleteUserSaleView.as_view()),
    path('delete/user_returns/<str:email>/', views.DeleteUserReturnsView.as_view()),
    path('delete/user_return/<str:data>/', views.DeleteUserReturnView.as_view()),
]

