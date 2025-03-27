from django.urls import path
from . import views
from django.http import HttpResponse


urlpatterns = [
    path('favicon.ico', lambda x: HttpResponse(status=204)),
    
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    
    path('', views.front, name="front"),
    path('home/', views.home, name="home"),
    
    path('update-user/', views.updateUser, name="update-user"),
    
    path('regions/<int:state_id>/', views.region_list, name='region_list'),
    path('region/<int:region_id>/', views.region_detail, name='region_detail'),
    
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    
    path('subscription/', views.subscription_page, name='subscription_page'),
    path('subscription/success/', views.subscription_success, name='subscription_success'),
    path('subscription/invoice/', views.subscription_invoice, name="subscription_invoice"),
    
    path('support/create/', views.create_request, name='create_request'),
    
    path('chatbot/<int:region_id>/', views.chatbot, name='chatbot'),
    
    
]