from django.urls import path

from . import views

urlpatterns=[
    path('',views.index, name='index'),
    path('customers/<str:customerId>/',views.customers, name='customers'),

    path('cust_create_order/<str:pk>/',views.Cust_CreateOrder, name='cust_create_order'),

    path('create_order/<str:pk>/',views.CreateOrder, name='create_order'),
    path('update_order/<str:pk>/',views.UpdateOrder, name='update_order'),
    path('delete_order/<str:dk>/',views.DeleteOrder, name='delete_order'),

    path('register/',views.RegisterPage, name='register'),
    path('adminRegister/',views.AdminRegisterPage, name='adminRegister'),
    path('login/',views.LoginPage, name='login'),
    path('logout/',views.LogoutPage, name='logout'),
    path('admin/',views.Admin, name='admin'),

    path('user/',views.UserPage, name='user'),
]