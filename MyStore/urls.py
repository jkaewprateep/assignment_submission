from django.urls import path
from MyStore import views

### Add
from django.urls import re_path as url;
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token;

urlpatterns = [
    
    ## Statics Paths
    path("", views.home, name="home"),
    path('about/', views.about, name="about"),
    path('Index/', views.index, name="index"),
    path('loginpage/', views.loginpage, name="loginpage"),
    path('menu/', views.menu, name="menu"),
    
    ### User and handles and user authentication
    url(r'^login/$', views.signin, name='login'),
    # url(r'^api-token-refresh/', refresh_jwt_token),
    # url(r'^api-token-verify/', verify_jwt_token),
    # url(r'^register/$', views.UserCreateAPIView.as_view(), name='register'),
    # url('users/', views.signin, name='login'),


    ## User / SiteID
    path('assignusersiteIDView/', views.assignusersiteIDView.as_view()),
    
    
    ## Products Query / Insert / Update
    path('product_update/', views.products, name='products'), 
    
    
    ## Promotions Query / Insert / Update
    path('promotion_update/', views.promotions, name='promotions'), 
    path('promotions_as_view/', views.promotions_as_view.as_view()),
    
    
    # Products Query with query string and conditions
    path('menu_items_as_view/', views.MenuView_as_view.as_view()),
    path('MenuView_readupdate_as_view/', views.MenuView_readupdate_as_view.as_view()),
    path('menu_items/', views.MenuView.as_view()),
    
]