from django.urls import path
from . import views

app_name = 'prompt'

urlpatterns = [
    path('', views.index, name='index'),
    ]