from django.urls import path,include
from . import views

app_name='api-v1'

urlpatterns=[
    path('registration/',views.RegistrationApiView.as_view(), name='registration'),
    path('token/login/',views.CustomAuthToken.as_view(),name='token-login'),
    path('token/logout/',views.CustomDiscardAuthToken.as_view(),name='token-logout')
]