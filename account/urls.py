from django.urls import path
from rest_framework import routers

from .views import (
    UserCreateViewSet, 
    ObtainAuthTokenView, 
    LogoutView,
    ChangePasswordvView
)


app_name = 'account'

router = routers.DefaultRouter()

router.register('user-sign-up', UserCreateViewSet, basename='user_sign_up')

urlpatterns=[
    path('user-login', ObtainAuthTokenView.as_view(), name='user_login'),
    path('user-logout', LogoutView.as_view(), name='user_logout'),
    path('change-password', ChangePasswordvView.as_view(), name='change_password')
]
urlpatterns += router.urls
