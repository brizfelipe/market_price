from django.urls import path
from . import views


urlpatterns = [
    path('api/<str:cep>',views.api,name='start'),
]