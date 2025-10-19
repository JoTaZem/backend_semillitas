from django.contrib import admin
from django.urls import path
from .viewsApi import *
from app_semillitas import viewsApi
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = {
    path('token/',CustomTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh',TokenRefreshView.as_view(),name='token_refresh'),
    path('administrador/', AdminList.as_view()),
    path('administrador/<int:pk>', AdminDetail.as_view()),
    path('jugador/', JugadorList.as_view()),
    path('jugador/<int:pk>',JugadorDetail.as_view()),
    path('evaluacion/',EvaluacionList.as_view()),
    path('nivel/', NivelList.as_view()),
    path('palabra/', PalabraList.as_view())
}