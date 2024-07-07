
from django.shortcuts import render
from django.templatetags.static import static
from .models import *
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from .forms import OrderForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
# import requests
# from alipay import AliPay
# from django.conf import settings
from django.http import JsonResponse
from .utils import *
import json
from django.db.models import Max
import markdown
import uuid

def chatPage(request):
    #检查登录状态
    user = getUser(request)
    if user is not None:#如果存在登录的用户
        return render(request,'chat-daylight.html')
    else :
        request.session.flush() #清空当前会话缓存
        return redirect('/signin')#退回到登录页

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
        # id = UserAccount.objects.count() + 1
        # 执行登录
        data=UserAccount(user_id=username,user_password=password,user_nikeName=nickname)
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
        
def ai_detail(request, ai_id):
    # 获取当前用户的用户ID，假设用户ID保存在 session 的 edit_id 中
    user_id = request.session.get("edit_id")
    
    # 查询所有与该 AI 相关的评论，并按时间降序排序
    all_talk = talk.objects.filter(follow=ai_id).order_by('-time')
    
    # 获取 AI 的信息
    imformation = ai.objects.filter(id=ai_id).first()
    
    # 准备一个字典来存储每条评论的点赞状态
    likes = {}
    
    # 遍历所有评论，检查当前用户是否已经点赞
    for x in all_talk:
        if user_id and great.objects.filter(user=user_id, talk=x.id).exists():
            likes[x.id] = True  # 如果当前用户已经点赞该评论，设置为 True
        else:
            likes[x.id] = False  # 如果当前用户未点赞该评论，设置为 False

    return render(request, "ai_detail.html", {
        'list': all_talk,
        'ai': imformation,
        'like': likes  # 将点赞状态传递给模板
    })


def ai_collect(request):   #用户收藏页面
    user_id  = request.session["edit_id"]   #用户id
    user = UserAccount.objects.filter(id = user_id).first()
    all_collect = favorite.objects.filter(user = user)

    sorted(all_collect,key=lambda x:x.time,reverse = True) #按照收藏时间排序 （最近收藏的靠前）#先排序

    list = []
    if user_id :   #解析为收藏ai的信息
        for x in all_collect:
            t = ai.objects.filter(id = int(x.ai.id)).first()
            list.append(t)
        return render(request ,"ai_collect.html",
                    {
                        'list' : list
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
                    'list' : list,
                    "rank" :1
                  }
                  )

def Creattalk(request):   
    # 执行需要执行的 Python 代码
    if request.method=='POST':  #获取相关信息
        Pfollow = int(request.POST.get('follow')) #这个确定不是跟随的主评论？
        Ptext = request.POST.get('text')
        Puser_id = request.session["edit_id"]   #用户id
        if Puser_id:
            if(Ptext == None):
                data = {'flag':False , 'Message':"文本信息不存在！"}  
            # 使用auth模块去auth_user表查找

            Puser = UserAccount.objects.filter(id = Puser_id).first()  #查找用户对象

            if Puser:
                Pfollownum = 0
                Pgreat = 0  #初始化\
                PgreatNum = 0
                #楼层号的分配 以及对应楼层/pid的分配  #这里先预定1-9999999号为ai id 其余为talk id
                if Pfollow  > 9999999 : #如果为跟评
                    
                    if talk.objects.filter(id = Pfollow).first():
                        Plevel  = 0  #不分配楼层号
                        #############################
                        #临时补丁
                        if talk.objects.aggregate(Max('id'))['id__max'] is not None:
                            Pid = talk.objects.aggregate(Max('id'))['id__max'] + 1
                        else:
                            Pid = 1
                        #补丁结束
                        #############################
                        Pusername = Puser.user_nikeName
                        x=talk(id= Pid,follow = Pfollow,user = Puser,username = Pusername,follownum = Pfollownum,text = Ptext,great = PgreatNum,greatNum = 0 ,level = Plevel)
                        x.save()   #上传评论信息
                        x = talk.objects.filter(id = Pfollow).first()
                        x.follownum += 1
                        x.save()
                        data = {'flag':True , 'Message':"成功评论！"}  
                    else:
                        data = {'flag':False , 'Message':"评论不存在！"}    
                else:  #如果为主评
                    Pai = ai.objects.filter(id = Pfollow).first()
                    #####################为什么要filter这个
                    print(Pfollow,Pai)
                    if Pai:
                        Pai.level = Pai.level + 1 #楼层号 + 1
                        Plevel = Pai.level
                        if talk.objects.aggregate(Max('id'))['id__max'] is not None:
                            Pid = talk.objects.aggregate(Max('id'))['id__max'] + 1
                        else:
                            Pid = 1
                        Pusername = Puser.user_nikeName
                        x=talk(id= Pid,follow = Pfollow,user = Puser,username = Pusername,follownum = Pfollownum,text = Ptext,great = PgreatNum,greatNum = 0 ,level = Plevel)
                        x.save()   #上传评论信息
                        data = {'flag':True , 'Message':"成功评论！"}   
                    else:
                        data = {'flag':False , 'Message':"ai不存在！"}     
            else:
                data = {'flag':False , 'Message':"用户不存在！"}         
        else:
            data = {'flag':False , 'Message':"请先登录！"}     
    else:
        data = {'flag':False , 'Message':"无效的请求！"}     
    return JsonResponse(data)  


def talkdelete(request):
    # 执行需要执行的 Python 代码
    print(1)
    if request.method=='POST':  #获取相关信息
        Pid = request.POST.get('talk')
        Puser = request.session["edit_id"]  #用户id信息
        print(Pid)
        if Puser:
            result = talk.objects.filter(id = Pid).first()  #查找到删除评论
            if str(result.user.id) == str(Puser):
                if ai.objects.filter(id = result.follow).first(): #如果为主评
                    results = talk.objects.filter(follow = Pid) #标记所有跟评
                    if results:
                        results.delete()  #删除所有跟评
                else:
                    maintalk = talk.objects.filter(id = result.follow).first()
                    maintalk.follownum -= 1
                    maintalk.save()   #主频回复-1
                result.delete()
                data = {'flag':True , 'Message':"已删除该评论！"}
            else:
                data = {'flag':False , 'Message':"删除账号与对话账号不一致！"}  
        else:
            data = {'flag':False , 'Message':"请先登录！"}   
    else:
        data = {'flag':False , 'Message':"无效的请求！"} 
    return JsonResponse(data)    

def followtalk(request,ai_id,talk_id):

    talks = talk.objects.filter(follow = talk_id)
    imformation  = talk.objects.filter(id = talk_id).first()
    sorted(talks,key=lambda x:x.time,reverse = True)   #先按照时间排序
    return render(request ,"ai_followtalk.html",
                    {
                        'list' : talks,
                        'talk' : imformation,
                        'ai' : ai_id
                    }
                    ) 

def greats(request):
    if request.method == 'POST':
        Puser = request.session["edit_id"]   # 获取用户id信息
        Ptalk = request.POST.get('talk')     # 获取评论id信息
        user = UserAccount.objects.filter(id=Puser).first()
        talk_obj = talk.objects.filter(id=Ptalk).first()

        if user and talk_obj:
            if great.objects.filter(user=user, talk=talk_obj).exists():
                # 用户已经点赞，取消点赞
                great.objects.filter(user=user, talk=talk_obj).delete()
                talk_obj.greatNum -= 1
                talk_obj.save()
            else:
                # 用户未点赞，进行点赞操作
                new_great = great(user=user, talk=talk_obj)
                new_great.save()
                talk_obj.greatNum += 1
                talk_obj.save()

            data = {'flag': True, 'Message': "操作成功！", 'greatNum': talk_obj.greatNum}
        else:
            data = {'flag': False, 'Message': "无效的用户或评论信息！"}

        return JsonResponse(data)
    else:
        return JsonResponse({'flag': False, 'Message': "无效的请求！"})


def collect(request):
    if request.method == 'POST':
        if 'edit_id' in request.session:  # 检查是否存在 edit_id
            Puser = request.session['edit_id']
            Pai = int(request.POST.get('ai_id'))
            user = UserAccount.objects.filter(id=Puser).first()
            tai = ai.objects.filter(id=Pai).first()  # 修改为首字母大写的模型名
            if user and tai:
                if favorite.objects.filter(user = user,ai=tai):
                    data = {'flag': False, 'Message': '已经收藏过了！'}
                else:
                    x = favorite(user=user, ai=tai)
                    x.save()
                    data = {'flag': True, 'Message': '已收藏！'}
            else:
                data = {'flag': False, 'Message': '用户或AI信息不存在！'}
        else:
            data = {'flag': False, 'Message': '请先登录！'}
    else:
        data = {'flag': False, 'Message': '无效的请求！'}
        
    return JsonResponse(data)


def deletecollect(request):
    if request.method=='POST':  #获取相关信息
        Puser = request.session["edit_id"] 
        Pai = request.POST.get('ai')
        Puser = UserAccount.objects.filter(id=Puser).first()
        Pai = ai.objects.filter(id=Pai).first()
        if Puser:
            result = favorite.objects.filter(user = Puser,ai = Pai).first()  #查找到相关信息
            if result:
                result.delete()
                data = {'flag':True , 'Message':"已删除该收藏！"}
            else:
                data = {'flag':False , 'Message':"该收藏不存在！"} 
        else:
            data = {'flag':False , 'Message':"无效的账号信息！"} 
    else:
        data = {'flag':False , 'Message':"无效的请求！"} 
    return JsonResponse(data)
    
def test(request): #单函数测试工具
    # engine1 = aiEngine(id=0,name='讯飞星火Spark Max',subname="强大的语言模型，效果好")
    # engine1.save()
    # engine1 = aiEngine(id=1,name='讯飞星火Spark Lite',subname="轻量级大语言模型，低延迟，全免费")
    # engine1.save()
    # engine1 = aiEngine(id=2,name='讯飞星火Spark Pro',subname="专业级大语言模型，兼顾模型效果与性能")
    # engine1.save()
    # engine1 = aiEngine(id=3,name='讯飞星火Spark 4.0 Ultra',subname="最强大的星火大模型版本，效果极佳")
    # engine1.save()
    # if request.session.get("id") is not None:
    #     id = request.session["id"]#另存id
    #     user = checkLoginByID(id)#获得用户
    #     return HttpResponse(modifyCredits(user=user,creditsChange=0))
    
    # user = getUser(request=request)
    # if user is not None:
    #     Testai = ai(0,'测试用Prompt简介',user.id,'所有者字段','简介字段')
    #     Testai.save()
    # ###################################
    # # 定义API的URL
    # url = 'http://127.0.0.1:8000/order/api/create_order/'

    # # 准备POST请求的数据
    # data = {
    #     'username': "114514",
    #     'product_id': 'product123',
    #     'amount': 99.9
    # }

    # # 发送POST请求
    # response = requests.post(url, data=data)

    # # 打印响应内容
    # print('Response Status Code:', response.status_code)
    # print('Response JSON:', response.json())
    # return HttpResponse(str(data["username"])+str(response.json()))
    # ###################################
    return HttpResponse("测试完毕")

def mainPage(request):#主页
    return render(request,"homePage.html")


def create_new_order(request):
    if request.method == 'GET':
        user_id = request.session.get("id")
        user = get_object_or_404(UserAccount, id=user_id)
        product_id = request.GET.get('product_id')
        amount = request.GET.get('amount')

        if not user or not product_id or not amount:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            order = Order(
                user=user,
                product_id=product_id,
                amount=amount,
                status='pending'
            )
            order.save()
            return redirect('order_detail', order_id=order.id)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def order_detail_view(request, order_id):
    # 根据订单号查询订单对象
    order = get_object_or_404(Order, id=order_id)
    
    # 可以根据具体的业务逻辑处理订单状态等信息
    # 例如，生成支付按钮的 URL 或处理支付逻辑

    return render(request, 'order_detail.html', {'order': order})

def my_orders(request):
    # 查询当前用户的所有订单
    user = UserAccount.objects.filter(id=request.session.get("id")).first()
    orders = Order.objects.filter(user=user)
    
    return render(request, 'my_orders.html', {'orders': orders})


def chatMessage(request):#用于对话流的实现,只接受POST
    data = {}
    if request.method == 'POST':
        data['status'] = 0
        if not request.content_type == 'application/json':
            return JsonResponse({'error': 'Content-Type must be application/json'}, status=400)

        try:
            # 尝试解析请求体为JSON
            data = json.loads(request.body)
            print(data)
            if data.get('message') is not None:#收到有效消息
                print('收到有效消息')
                data['status'] = 1
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
        returnContent = {'status':'fail'}
        if data['status']:#收到有效消息：
            returnContent['status'] = 'success'
            #处理消息流

            returnContent['message'] =markdown.markdown('#返回消息') 
            return JsonResponse(returnContent)
        #input_data = data.get('data', '')

        # 这里可以对输入的数据进行处理，例如保存到数据库、进行计算等
        #processed_data = f"You entered: {input_data}"

        # 返回JSON响应
        return JsonResponse({'status':'success'})#{'processed_data': processed_data})
    


