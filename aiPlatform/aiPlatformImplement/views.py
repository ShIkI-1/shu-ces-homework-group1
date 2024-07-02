
from django.shortcuts import render
from django.templatetags.static import static
from .models import *
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse

def chatPage(request):
    #检查登录状态

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
        
def ai_detail(request,ai_id): #详情页
    all_talk = talk.objects.filter(follow = ai_id)
    imformation = ai.objects.filter(id = ai_id).first()
    if all_talk:       #主评显示
        sorted(all_talk,key=lambda x:x.time,reverse = True)   #先按照时间排序
        max5 = []
        for i in range(5):
            tmax = max(all_talk,key = lambda x:x.greatNum)
            max5.append(tmax)   

        sorted(max,key=lambda x:x.greatNum,reverse = True)
        all_talk = max5.extend(all_talk) #排序 默认前五个点赞高 后面全为最新靠前    
        
    return render(request ,"ai_detail.html",   
                  {
                    'list' : all_talk,
                    'ai' : imformation          
                  }
    )

def ai_collect(request):   #用户收藏页面
    user_id  = request.session["edit_id"]   #用户id
    all_collect = favorite.objects.all(user = user_id)
    if user_id :
        sorted(all_collect,key=lambda x:x.time,reverse = True) #按照收藏时间排序 （最近收藏的靠前）
        return render(request ,"ai_collect.html",
                    {
                        'list' : all_collect
                    }
                    )
    else:
        return render(request,'ai_collect.html',{"error":"请先登录!"})    

def ai_list(request):  #排行榜
    list = ai.objects.all()  #存放所有ai  #没有ai表 没写  
        
    sorted(list,key=lambda x:x.marks,reverse = True) #分数排序
    list = list[:50]
    return render(request ,"ai_list.html",
                  {
                    'list' : list
                  }
                  )



def Creattalk(request):   
    # 执行需要执行的 Python 代码
    if request.method=='POST':  #获取相关信息
        Pfollow = request.POST.get('follow')
        Ptext = request.POST.get('text')

        Puser = request.session["edit_id"]   #用户id
        if Puser:
            if(Ptext == None):
                return render(request, "ai_details.html", {"error":"文本信息不存在"})
            # 使用auth模块去auth_user表查找

            Pfollownum = 0
            Pgreat = 0  #初始化

            result = UserAccount.objects.filter(id = Puser).first()
            flag  = 1 #标志位 对应评论/ai是否存在
            if result:
                #楼层号的分配 以及对应楼层/pid的分配  #这里先预定1-9999999号为ai id 其余为talk id
                if Pfollow  > 9999999 : #如果为跟评
                    if talk.objects.filter(id = Pfollow).first():
                        Plevel  = 0  #不分配楼层号
                    else:
                        return render(request,"ai_detail.html",{"error":"评论不存在！"})    
                        flag = 0 
                else:  #如果为主评
                    ai = ai.objects.filter(id = Pfollow)   #查找对应ai
                    if ai:
                        ai.level = ai.level + 1 #楼层号 + 1
                        Plevel = ai.level
                    else:
                        return render(request,"ai_detail.html",{"error":"ai不存在！"})    
                        flag = 0 
                if flag:
                    Pid =  10000000 + len(talk.objects.all()) #分配id
                    Pusername = result.user_nikeName
                    x=talk(id= Pid,follow = Pfollow,user = Puser,username = Pusername,follownum = Pfollownum,text = Ptext,great = Pgreat,level = Plevel,username = Pusername)
                    x.save()   #上传评论信息
                    return render(request,"ai_detail.html")
            else:
                return render(request,"ai_detail.html",{"error":"用户不存在！"})    
        else:
            return render(request,"ai_detail.html",{"error":"请先登录！"})  
    else:
        return render(request,"ai_detail.html",{"error":"无效的请求！"})   
    
#def followtall(request): 跟评显示

def great(request):
    # 执行需要执行的 Python 代码
    if request.method=='POST':  #获取相关信息
        Puser = request.session["edit_id"]  #用户id信息
        Ptalk = request.POST.get('talk')
        if Puser:
            if great.objects.filter(user = Puser,talk = Ptalk).first():
                return render(request,"ai_detail.html",{"error":"不能重复点赞！"})
            else:   
                result = talk.objects.filter(id = Ptalk).first()  #查找到相关信息
                if result:  
                    result.greatNum = result.greatNum + 1 #自动+1
                    data = great(user = Puser,talk = Ptalk) #创建信息 便于管理
                    data.save()
                    return render(request,"ai_detail.html")
                else:
                     return render(request,"ai_detail.html",{"error":"无效的对话信息！"})
        else:
            return render(request,"ai_detail.html",{"error":"请先登录！"})    
    else:
        return render(request,"ai_detail.html",{"error":"无效的请求！"}) 

def deletegreat(request):
    # 执行需要执行的 Python 代码
    if request.method=='POST':  #获取相关信息
        Puser = request.session["edit_id"]  #用户id信息
        Ptalk = request.POST.get('talk')
        if Puser:
            x = talk.objects.filter(id = Ptalk).first()
            if x:  #查找到相关信息
                result = great.objects.filter(user = Puser,talk = Ptalk).first()
                if result:  
                    x.greatNum = x.greatNum - 1 #自动-1
                    result.delete()
                    return render(request,"ai_detail.html")
                else:    
                    return render(request,"ai_detail.html",{"error":"用户未点赞！"})  
            else:
                return render(request,"ai_detail.html",{"error":"无效的对话信息！"})   
        else:
            return render(request,"ai_detail.html",{"error":"请先登录！"})   
    else:
        return render(request,"ai_detail.html",{"error":"无效的请求！"}) 

def talkdelete(request):
    # 执行需要执行的 Python 代码
    if request.method=='POST':  #获取相关信息
        Pid = request.POST.get('id')
        Puser = request.session["edit_id"]  #用户id信息
        if Puser:
            result = talk.objects.filter(id = Pid).first()  #查找到删除评论
            if result.user == Puser:
                result.delete()
                return render(request,"ai_detail.html")
            else:
                return render(request,"ai_detail.html",{"error":"请求账号与对话账号不一致！"}) 
        else:
            return render(request,"ai_detail.html",{"error":"请先登录！"})  
    else:
        return render(request,"ai_detail.html",{"error":"无效的请求！"})

def collect(request):
    if request.method=='POST':  #获取相关信息
        Puser = request.session["edit_id"] 
        Pai = request.POST.get('ai')
        if Puser:
            X = favorite(user = Puser,ai = Pai)
            X.save()
            return render(request,"ai_detail.html")
        else:
            return render(request,"ai_detail.html",{"error":"请先登录！"})
    else:
       return render(request,"ai_detail.html",{"error":"无效的请求！"})

def deletecollect(request):
    if request.method=='POST':  #获取相关信息
        Puser = request.session["edit_id"] 
        Pai = request.POST.get('ai')
        if Puser:
            result = favorite.objects.filter(user = Puser,ai = Pai).first()  #查找到相关信息
            if result:
                result.delete()
                return render(request,"ai_collect.html")
            else:
                return render(request,"ai_collect.html",{"error":"该收藏不存在！"})
        else:
            return render(request,"ai_collect.html",{"error":"无效的账号信息！"})
    else:
        return render(request,"ai_collect.html",{"error":"无效的请求！"})
    
def test(request): #单函数测试工具
    # engine1 = aiEngine(id=1,name='讯飞星火Spark Lite',subname="轻量级大语言模型，低延迟，全免费")
    # engine1.save()
    # engine1 = aiEngine(id=2,name='讯飞星火Spark Pro',subname="专业级大语言模型，兼顾模型效果与性能")
    # engine1.save()
    # engine1 = aiEngine(id=3,name='讯飞星火Spark 4.0 Ultra',subname="最强大的星火大模型版本，效果极佳")
    # engine1.save()
    return HttpResponse("暂无测试内容")

def mainPage(request):#主页
    return render(request,"homePage.html")
