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
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from aiPlatformImplement import views

urlpatterns = [
    path('chat', views.chatPage),
    path('signin', views.login, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signupto', views.signupto, name='signupto'),
    path('admin/users', views.adminuser),
    path('loginCheck', views.loginCheck, name='loginCheck'),
    path('prompt',views.promptIndex, name='index'),
    path('prompt/pub',views.pub_ai),
    path('useredit',views.useredit, name='useredit'),
    path('edituserto', views.edituserto, name='edituserto'),
    path('userdetail', views.userdetail, name='userdetail'),
    path('chat/test',views.test),
    path('',views.mainPage, name='home'),
    path('prompt/list',views.ai_list),
    path('prompt/detail/<int:ai_id>',views.ai_detail),
    path('prompt/collect',views.ai_collect),
    path('creattalk',views.Creattalk,name='creattalk'),
    path('collect',views.collect,name = 'collect'),
    path('buyaiprompt',views.buyaiprompt,name = 'buyaiprompt'),
    path('deletetalk',views.talkdelete,name = 'deletetalk'),
    path('great',views.greats,name = 'great'),
    path('deletecollect',views.deletecollect,name = 'deletecollect'),
    path('order/<str:order_id>/', views.order_detail_view, name='order_detail'),
    path('order/api/create_order/', views.create_new_order, name='create_new_order'),
    path('my_orders', views.my_orders, name='my_orders'),
    # path('return/', views.payment_return, name='payment_return'),  # 支付宝支付成功后的回调URL
    path('chatMessage',views.chatMessage),
    path('prompt/detail/<int:ai_id>/<int:talk_id>',views.followtalk),
    path('prompt/myprompt',views.my_prompt),
    path('prompt/rate/<int:ai_id>',views.rate),
    path('clear',views.clearLogin),
    path('order/payment',views.payment,name='payment'),
    path('alipay/notify/', views.alipay_notify, name='alipay_notify'),
    path('personalindex',views.personalindex,name='personalindex'),
    path('prompt/usage/<int:prompt_id>',views.usage,name='usage'),
    path('chat/buy',views.buyEngine),
    path('prompt/charge',views.charge,name = 'charge'),
    path('recharge-success/', views.recharge_success, name='recharge_success'),
    path('prompt/mypurchase',views.my_purchase,name='my_purchase'),
    path('prompt/myadmin',views.myadmin,name='myadmin')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
