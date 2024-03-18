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
    path('add/user_department/<str:email>/<str:data>/', views.AddUserDepartmentView.as_view()),
    path('add/user_employer/<str:email>/<str:data>/', views.AddUserEmployeeView.as_view()),
    path('add/user_markup/<str:email>/<str:data>/', views.AddUserMarkupView.as_view()),
    path('add/user_product', views.AddUserProductView.as_view()),
    # path('add/user_sale/<str:email>/<str:data>/', views.AddUserSaleView.as_view()),
    # path('add/user_return/<str:email>/<str:data>/', views.AddUserReturnView.as_view()),
]

# {"uid": 111, "name": "Майка", "quantity": 412, "description": "крутая футболка", "price_purchasing": 100, "price_retail": 150, "price_wholesale": 200, "price_agent": 100, "options": [{"color": "Синий", "size": "50", "quantity": 2, "storage": "ящик 1", "price_purchasing": 100, "price_retail": 200, "price_wholesale": 150, "price_agent": 150}]}

