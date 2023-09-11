from django.urls import path
from user_app import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('api/user/register/', views.user_registration, name='user_registration'),
    path('api/user/login/', views.user_login, name='user_login'),
]
