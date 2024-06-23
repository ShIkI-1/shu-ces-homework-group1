from .models import UserAccount
from django.shortcuts import render,redirect
from django.contrib import auth

def login(request):
    return render(request,"login.html")

def adminuser(request):

    return render(request,"adminusers.html")

def execute_code(request):
    # 执行需要执行的 Python 代码
    if request.method=='POST':

        username = request.POST.get('username') #获取POST中的username
        password = request.POST.get('password') #获取POST中的username
        
        if(username == None or password == None):
            return render(request, "login.html", {"error":"请填写账号或密码"})
        # 使用auth模块去auth_user表查找
        result = UserAccount.objects.filter(user_id=username, user_password=password).first()
        print(result)
        if not result:
            return render(request, "login.html", {"error": "账号或密码输入有误"})
        request.session["username"] = username
        # 执行登录
        return redirect(request, "result.html")
      

        
from django.templatetags.static import static

