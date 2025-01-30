from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name='api-v1'

urlpatterns=[
    # registration
    path('registration/',views.RegistrationApiView.as_view(), name='registration'),

    # verification
    path('send-mail/',views.TestEmailSend.as_view(),name='send-mail'),

    # change password
    path('changed-password/', views.ChangePasswordApiView.as_view(),name='change-password'),

    # login token
    path('token/login/',views.CustomAuthToken.as_view(),name='token-login'),
    path('token/logout/',views.CustomDiscardAuthToken.as_view(),name='token-logout'),

    # login jwt
    path('jwt/create/',TokenObtainPairView.as_view(),name='jwt-create'),
    path('jwt/refresh/',TokenRefreshView.as_view(),name='jwt-refresh'),
    path('jwt/verify/',TokenVerifyView.as_view(),name='jwt-verify'),

    # profile
    path('profile/',views.ProfileApiView.as_view(),name='profile'),
]