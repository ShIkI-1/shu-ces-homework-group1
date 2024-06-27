
from django.shortcuts import render
from django.templatetags.static import static
from .models import UserAccount
from django.shortcuts import render,redirect




def chatPage(request):
    return render(request,'chat-daylight.html')
    #return render(request,'chat.html')


def login(request):
    return render(request,"login.html")

def signup(request):
    return render(request,"signup.html")

def adminuser(request):
    users = UserAccount.objects.all()

    
    return render(request,"adminusers.html",{"users":users})

def loginCheck(request): #登录检查
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
        request.session["id"] = str(result.id)
        # 执行登录
        return redirect('/userdetail',method='POST')
    
def signupto(request):
    # 执行需要执行的 Python 代码
    if request.method=='POST':
        nickname = request.POST.get('nickname') #获取POST中的username
        username = request.POST.get('username') #获取POST中的username
        password = request.POST.get('password') #获取POST中的username
        print(username)
        if(username == None or password == None):
            return render(request, "login.html", {"error":"请填写账号或密码"})
        # 使用auth模块去auth_user表查找
        result = UserAccount.objects.filter(user_id=username).first()
        print(result)
        if result:
            return render(request, "signup.html", {"error": "账号已存在"})
        id = UserAccount.objects.count() + 1
        # 执行登录
        data=UserAccount(id=id,user_id=username,user_password=password,user_nikeName=nickname)
        data.save()
        return render(request, "login.html")   

def pub_ai(request):
    
    return render(request,"pub_ai.html")
        

def promptIndex(request):
    return render(request, 'index.html')

def useredit(request):
    if request.method=='POST':
        id=request.POST.get('id')
        result = UserAccount.objects.filter(id=id).first()
        if result:
            request.session["edit_id"] = id
            return render(request,"edituser.html")
        else :
            return render(request,"adminusers.html",{"error":"用户不存在"})
    else :
            return render(request,"adminusers.html",{"error":"用户不存在"})
    
def edituserto(request):
    if request.method == 'POST':
        id = request.session.get("edit_id")
        nickname = request.POST.get('nickname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        result = UserAccount.objects.filter(id=id).first()
        if result:
            result.user_nikeName = nickname
            result.user_id = username
            result.user_password = password
            result.save()
            if request.path == '/user/edit':
                return redirect('/userdetail')
            else:
                return redirect('/admin/users')
        else:
            return render(request, "adminusers.html", {"error": "用户不存在"})
    else:
        return render(request, "adminusers.html", {"error": "无效的请求"})

def userdetail(request):
    id = request.session.get("id")
    user = UserAccount.objects.filter(id=id).first()
    return render(request,"userdetail.html",{"user":user})
        

    
