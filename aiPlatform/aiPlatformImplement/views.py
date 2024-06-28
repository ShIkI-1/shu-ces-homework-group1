
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
        

    
def ai_detail(request): #详情页
    return render(request,'ai_detail.html')

def ai_favorite(request):   #用户收藏页面
    return render(request,'ai_favorite.html')

def ai_list(request):  #排行榜
    return render(request,'ai_list.html')

def data_detail(request):    #测试版
    list = []  #存放当前ai下所有评论
    all_talk = talk.objects.all()
    sorted(list,key=lambda x:x.time,reverse = True)   #先按照时间排序
                                                
    def  great(x):
        return x.great

    max5 = []
    for i in range(5):
        tmax = max(list,key = lambda x:great(x))
        max5.append(x)   

    sorted(max,key=lambda x:x.great,reverse = True)
    list = max5.extend(list) #排序 默认前五个点赞高 后面全为最新靠前
    imformation = ai.objects.all()[0]

    pack = [list,imformation] 
    return render(request ,"aiPlatform/template/ai_detail.html",
                  {
                    'list' : pack          
                  }
                  )
'''
def data_detail(request,ai_id):    #这里 x.userx需要更换为username（目前为userid)  
    imformation = {} #存放ai相关信息
    list = []  #存放当前ai下所有评论
    all_talk = talk.objects.all()
    for x in all_talk:
        if x.follow == ai_id:
            list.append(x)
    sorted(list,key=lambda x:x.time,reverse = True)   #先按照时间排序
                                                
    def  great(x):
        return x.great

    max5 = []
    for i in range(5):
        tmax = max(list,key = lambda x:great(x))
        max5.append(x)   

    sorted(max,key=lambda x:x.great,reverse = True)
    list = max5.extend(list) #排序 默认前五个点赞高 后面全为最新靠前

    pack = [list,imformation] 
    return render(request ,"aiPlatform/template/ai_detail.html",
                  {
                    'list' : pack          
                  }
                  )
'''

def data_favorite(request):
    all_favoirte = favorite.objects.all() #测试版
    list = []  #存放当前用户下所有的收藏ai

    sorted(list,key=lambda x:x.time,reverse = True) #按照收藏时间排序 （最近收藏的靠前）

    return render(request ,"aiPlatform/template/ai_favorite.html",
                  {
                    'list' : list
                  }
                  )


'''
def data_favorite(request,user_id):
    all_favoirte = favorite.objects.all()
    list = []  #存放当前用户下所有的收藏ai

    for x in all_favoirte:
        if x.user == user_id:
            list.append(x)

    sorted(list,key=lambda x:x.time,reverse = True) #按照收藏时间排序 （最近收藏的靠前）

    return render(request ,"aiPlatform/template/ai_favorite.html",
                  {
                    'list' : list
                  }
                  )
'''

def data_list(request):  #先不管

    list = ai.objects.all()  #存放所有ai  #没有ai表 没写  
        
    sorted(list,key=lambda x:x.marks,reverse = True) #分数排序

    return render(request ,"aiPlatform/template/ai_list.html",
                  {
                    'list' : list[:50]   #切片操作 只取前50个
                  }
                  )