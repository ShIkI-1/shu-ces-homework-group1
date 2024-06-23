"""
URL configuration for aiPlatform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from aiPlatform import views
urlpatterns = [
    path('', views.chatPage),
    path('signin', views.login),
    path('signup', views.signup, name='signup'),
    path('signupto', views.signupto, name='signupto'),
    path('admin/users', views.adminuser),
    path('execute', views.execute_code, name='execute'),
    path('prompt',include('prompt.urls')),
    path('prompt/pub',views.pub_ai)
]
