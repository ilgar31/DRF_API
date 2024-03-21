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
    path('add/user/', views.AddUserView.as_view()),
    path('add/department/', views.AddUserDepartmentView.as_view()),
    path('add/employer/', views.AddUserEmployeesView.as_view()),
    path('add/markup/', views.AddUserMarkupView.as_view()),
    path('add/product/', views.AddUserProductView.as_view()),
    path('add/sale/', views.AddUserSaleView.as_view()),
    path('add/return/', views.AddUserReturnView.as_view()),
    #delete
    path('delete/user/', views.DeleteUserView.as_view()),
    path('delete/user_departments/', views.DeleteUserDepartmentsView.as_view()),
    path('delete/department/', views.DeleteUserDepartmentView.as_view()),
    path('delete/user_employees/', views.DeleteUserEmployeesView.as_view()),
    path('delete/employer/', views.DeleteUserEmployerView.as_view()),
    path('delete/user_markups/', views.DeleteUserMarkupsView.as_view()),
    path('delete/markup/', views.DeleteUserMarkupView.as_view()),
    path('delete/user_products/', views.DeleteUserProductsView.as_view()),
    path('delete/product/', views.DeleteUserProductView.as_view()),
    path('delete/user_sales/', views.DeleteUserSalesView.as_view()),
    path('delete/sale/', views.DeleteUserSaleView.as_view()),
    path('delete/user_returns/', views.DeleteUserReturnsView.as_view()),
    path('delete/return/', views.DeleteUserReturnView.as_view()),
    # update
    path('update/user/', views.UpdateUserView.as_view()),
    path('update/department/', views.UpdateDepartmentView.as_view()),
    path('update/employer/', views.UpdateEmployerView.as_view()),
    path('update/markup/', views.UpdateMarkupView.as_view()),
    path('update/product/', views.UpdateProductView.as_view()),
    path('update/sale/', views.UpdateSaleView.as_view()),
    path('update/return/', views.UpdateReturnView.as_view()),
]

