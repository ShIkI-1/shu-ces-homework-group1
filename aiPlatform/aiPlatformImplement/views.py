
from django.shortcuts import render
from django.templatetags.static import static
from pip._vendor.rich.prompt import Prompt
from urllib.parse import urlparse, urlunparse
from .models import *
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from .forms import *
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
import logging
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
import html
from django.http import JsonResponse
from .utils import *
import json
from django.db.models import Max
import markdown
import uuid
from .forms import promptform
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import rating


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')





def chatPage(request):
    #检查登录状态
    
    content = {}
    if request.method == 'GET':
        engineID = request.GET.get('engineID')
        if engineID is None:
            return redirect('')
        historyIndexID = request.GET.get('historyID')#获得历史列表
        promptID = request.GET.get('promptID')#获得使用的prompt
    else:
        return redirect('')

    user = getUser(request)
    if user is None:#如果存在登录的用户
        request.session.flush() #清空当前会话缓存
        return redirect('/signin')#退回到登录页
    if promptID is None:
        promptID = -1
    engineID = int(engineID) 
    engine = aiEngine.objects.get(id=engineID) #获得当前使用的engine
    historyList = chatHistoryIndex.objects.filter(user=user,engineID=engine).order_by('-createTime')[:15]
    passHistory = []#查询历史记录
    passHistory.clear()
    full_url = request.build_absolute_uri()
    
    print(full_url)
    
    # 解析URL
    parsed_url = urlparse(full_url)
    
    # 移除查询参数
    url_without_query = urlunparse(parsed_url._replace(query=""))
    content['curl'] = url_without_query+'?engineID='+str(engineID)
    url_without_query = url_without_query+'?promptID='+str(promptID)+'&engineID='+str(engineID)+'&historyID='

    for i in historyList: #对象构建
        historyItem = {}
        historyItem["title"] = i.title
        historyItem['id']=url_without_query+str(i.id)
        passHistory.append(historyItem)
        
    print(passHistory)
    content['historyList']=passHistory
    #接下来：如果传入了历史，则获取聊天记录
    
    passHistoryContent = []
    content['historyContent'] = passHistoryContent
    passHistoryContent.clear()
    if historyIndexID is not None and is_valid_uuid4(historyIndexID):
        index = chatHistoryIndex.objects.get(id=historyIndexID) #获得index对象
        if index is not None: #有效
            chatContent = chatHistoryContent.objects.filter(indexID=index).order_by('messageID')
            for i in  chatContent:
                contentItem = {}
                contentItem['role'] = i.role
                contentItem['message'] = markdown.markdown(html.escape(i.chatContent)) #进行md转换
                passHistoryContent.append(contentItem)
            #构造字典
            print(passHistoryContent)
            content['historyContent'] = passHistoryContent
            



    return render(request,'chat-daylight.html',content)

        
    #return render(request,'chat.html')


def login(request):
    user = getUser(request)
    if user is not None:#如果存在登录的用户
        return redirect('/userdetail')
    else :
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
    if request.method == 'POST':
        form = promptform(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            intro = form.cleaned_data.get('intro')
            text = form.cleaned_data.get('text')
            flexibility = form.cleaned_data.get('flexibility')
            randomness = form.cleaned_data.get('randomness')
            pid = prompt.objects.count() + 1
            user = getUser(request)
            prom = prompt.objects.create(pid=pid, title=title, flexibility=flexibility, randomness=randomness,
                                         text=text,
                                         intro=intro, user=user)
            ai.objects.create(id=pid, name=title, user=user, owner=user.user_id, brief=intro, prompt=prom)
            return JsonResponse({"code": 200, "message": "发布成功！"})

        else:
            print(form.cleaned_data)
            print(form.errors)
            return JsonResponse({"code": 400, "message": "shibai!"})
    elif request.method == 'GET':
        return render(request, "pub_ai.html")


def my_prompt(request):
    if request.method == 'GET':
        user = getUser(request)
        prompts = prompt.objects.filter(user=user)
        return render(request, 'myprompt.html', context={"prompts": prompts})
    elif request.method == 'POST':
        prompt_id = request.POST.get('prompt_id')
        prompt.objects.get(pid=prompt_id).delete()
        return redirect('/prompt/myprompt')


def rate(request, ai_id):
    my_ai = ai.objects.get(id=ai_id)
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        rid = rating.objects.count() + 1
        user = getUser(request)
        # 保存评分，具体实现根据你的Rating模型
        rating_instance, created = rating.objects.get_or_create(
            user=user,
            aif=my_ai,
            defaults={'value': rating_value}
        )
        if not created:
            rating_instance.value = rating_value
            rating_instance.save()

        return redirect('/prompt')
    elif request.method == 'GET':
        return render(request, 'rate.html', {"ai": my_ai})


def promptIndex(request):
    ais = ai.objects.all()
    return render(request, 'index.html', context={"ais": ais})


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
        avatarindex = request.POST.get('avatarindex')
        
        result = UserAccount.objects.filter(id=id).first()
        if result:
            result.user_nikeName = nickname
            result.user_id = username
            result.user_password = password
            result.avaterindex = avatarindex
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

    user = getUser(request)  #获取登录状态
    
    if user is None:  #如果未登录
        username = ''
        user_id = 0
    else:
        user_id = user.id
        username = user.user_nikeName
    
    # 查询所有与该 AI 相关的评论，并按时间降序排序
    all_talk = talk.objects.filter(follow=ai_id).order_by('-time')
    # 获取 AI 的信息
    imformation = ai.objects.filter(id=ai_id).first()
    
    # 准备一个字典来存储每条评论的点赞状态
    likes = {}
    
    # 遍历所有评论，检查当前用户是否已经点赞
    for x in all_talk:
        if user_id and great.objects.filter(user=user_id, talk=x.id).exists():  #如果用户登录
            likes[x.id] = True  # 如果当前用户已经点赞该评论，设置为 True
        else:
            likes[x.id] = False  # 如果当前用户未点赞该评论，设置为 False
    return render(request, "ai_detail.html", {
        'list': all_talk,
        'ai': imformation,
        "like" : likes,   # 将点赞状态传递给模板
        "username" :username   #转递登录用户相关信息 如果为空那就是未登录
    })


from django.shortcuts import render

def ai_collect(request):   #用户收藏页面
    if getUser(request):
        user_id  = getUser(request).id
        user = UserAccount.objects.filter(id = user_id).first()
        all_collect = favorite.objects.filter(user = user)

        sorted(all_collect,key=lambda x:x.time,reverse = True) #按照收藏时间排序 （最近收藏的靠前）#先排序

        list = []
        for x in all_collect:
            t = ai.objects.filter(id = int(x.ai.id)).first()
            list.append(t)
        return render(request ,"ai_collect.html",
                    {
                        'list' : list
                    }
                    )
    else:
        return render(request,'signup.html',{"error":"请先登录!"})    

def ai_list(request):  #排行榜
    list = ai.objects.filter().order_by('-marks')
    list = list[:50]
    return render(request ,"ai_list.html",
                  {
                    "list": list
                  }
                  )

def Creattalk(request):   
    # 执行需要执行的 Python 代码
    if request.method=='POST':  #获取相关信息
        Pfollow = int(request.POST.get('follow')) #这个确定不是跟随的主评论？
        Ptext = request.POST.get('text')
        Pfollowflag = int(request.POST.get('followflag'))
        if getUser(request) :
            Puser_id = getUser(request).id
            if Ptext:
                data = {'flag':False , 'Message':"文本信息不存在！"}  
            # 使用auth模块去auth_user表查找

            Puser = UserAccount.objects.filter(id = Puser_id).first()  #查找用户对象
            if Puser:
                Pfollownum = 0
                PgreatNum = 0
                if Pfollowflag : #如果为跟评
                    if talk.objects.filter(id = Pfollow).first():
                        Plevel  = 0  #不分配楼层号
                        Pusername = Puser.user_nikeName
                        Pid = talk.objects.aggregate(Max('id'))['id__max'] + 1
                        x=talk(id= Pid,follow = Pfollow,user = Puser,username = Pusername,follownum = Pfollownum,text = Ptext,great = PgreatNum,greatNum = 0 ,level = Plevel,followflag = Pfollowflag)
                        x.save()   #上传评论信息
                        data = {'flag':True , 'Message':"成功评论！",'username':x.username,'time':x.time,'id':x.id}
                        x = talk.objects.filter(id = Pfollow).first()
                        x.follownum += 1
                        x.save()  
                    else:
                        data = {'flag':False , 'Message':"评论不存在！"}    
                else:  #如果为主评
                    Pai = ai.objects.filter(id = Pfollow).first()
                    if Pai:
                        Pai.level = Pai.level + 1 #楼层号 + 1
                        Plevel = Pai.level
                        if talk.objects.aggregate(Max('id'))['id__max'] is not None:
                            Pid = talk.objects.aggregate(Max('id'))['id__max'] + 1
                        else:
                            Pid = 1
                        Pusername = Puser.user_nikeName
                        x=talk(id= Pid,follow = Pfollow,user = Puser,username = Pusername,follownum = Pfollownum,text = Ptext,great = PgreatNum,greatNum = 0 ,level = Plevel,followflag = Pfollowflag)
                        x.save()   #上传评论信息
                        data = {'flag':True , 'Message':"成功评论！",'username':x.username,'time':x.time,'id':x.id} 
                    else:
                        data = {'flag':False , 'Message':"ai不存在!"}     
            else:
                data = {'flag':False , 'Message':"用户不存在！"}         
        else:
            data = {'flag':False , 'Message':"请先登录！"}     
    else:
        data = {'flag':False , 'Message':"无效的请求！"}     
    return JsonResponse(data)  


def talkdelete(request):
    # 执行需要执行的 Python 代码
    if request.method=='POST':  #获取相关信息
        Pid = request.POST.get('talk')
        if getUser(request):
            Puser = getUser(request).id
            result = talk.objects.filter(id = Pid).first()  #查找到删除评论
            if str(result.user.id) == str(Puser):
                if int(result.followflag) == 0: #如果为主评
                    results = talk.objects.filter(follow = Pid,followflag = 1) #标记所有跟评
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
        if getUser(request) :
            Puser = getUser(request).id  # 获取用户id信息
            Ptalk = request.POST.get('talk')     # 获取评论id信息
            user = UserAccount.objects.filter(id=Puser).first()
            talk_obj = talk.objects.filter(id=Ptalk).first()

            if user and talk_obj:
                if great.objects.filter(user=user, talk=talk_obj).exists():
                    # 用户已经点赞，取消点赞
                    great.objects.filter(user=user, talk=talk_obj).delete()
                    talk_obj.greatNum -= 1
                    liked = False
                    talk_obj.save()
                else:
                    # 用户未点赞，进行点赞操作
                    new_great = great(user=user, talk=talk_obj)
                    new_great.save()
                    talk_obj.greatNum += 1
                    liked = True
                    talk_obj.save()

                data = {'flag': True, 'Message': "操作成功！", 'greatNum': talk_obj.greatNum,'liked':liked}
            else:
                data = {'flag': False, 'Message': "无效的用户或评论信息！"}
        else:
            data = {'flag': False, 'Message': '请先登录！'}
        return JsonResponse(data)
    else:
        return JsonResponse({'flag': False, 'Message': "无效的请求！"})


def collect(request):
    if request.method == 'POST':
        if 'id' in request.session:  # 检查是否存在 edit_id
            if getUser(request) is None:
                return redirect('/signin')
            Puser = getUser(request).id
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
        if getUser(request) is None:
            return redirect('/signin')
        Puser = getUser(request).id
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

    return HttpResponse("测试完毕")

def mainPage(request):#主页
    return render(request,"homePage.html")


def create_new_order(request):
    if request.method == 'GET':
        user_id = request.session.get("id")
        user = get_object_or_404(UserAccount, id=user_id)
        product_id = request.GET.get('product_id')
        amount = request.GET.get('amount')
        address = request.GET.get('return_url')
        if not user or not product_id or not amount:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            order = Order(
                user=user,
                product_id=product_id,
                amount=amount,
                status='pending',
                return_url=address
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

def payment(request):
    order_id = request.GET.get('order_id')
    product_id = request.GET.get('product_id')
    amount = request.GET.get('amount')
    address = request.GET.get('return_url')
    # 实例化客户端
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '9021000138601835'
    alipay_client_config.app_private_key = 'MIIEpgIBAAKCAQEA8LNH7i4jvRBIT7sQVSgc5zZVHfI3CAaseu8QfsRjsdTgHVzAz19ZlWmFiobv7HcvS0SFDxdgMQ+IgiRXLfEUXQyBHXk8kVjXchUoQs57POn2phGvn4iFECQ1FGJQtVCi7RVQU+yMRLr6gsdY1BF1WapwpS5bhXCZXvoXOoN38HuRzHjfMo714wuXjzYN6w8MI4GSBACv/zuq94phd21xy4O7QIblqtZXCTnWiYwUqcTmX0vqR0I0sHEoQHhPb5Pz02yfibn67DKQFpiZ0U0Ygf9ta8SAI+O4yMPjWWiYUDrNlQeDik+oP8qdjlInqFQ3PBcfhrKmYi0QFO1QgNvFkwIDAQABAoIBAQCmcAHME8GIqWqnHz3S9JLP2kUPGP6uoRbBRu/MCHa7b+yswQdeHZuvcjDyMg5TH7LnQ/ESF2LfadNF0mUqEmq3UL8zJzMXeiw36aNWVrrmyw1PlikvklIYcED34GfYiHKwp61M6uOvXu98YOXudkgEAZQ01BJa+hpDj4FiZ6gW87PSHt7f0zoncgeEtdm2fvn5BCkkgiXiPoEbDjljWscP/eaxeTuZyNYLob+u3p8peI/8QCtrlUPV0kDIV+EhEOVzl0Z8fzvJM+wNWNUBuW8hXy2s0pFeh+cndid/z94iyC0LJTJ+FLGspFh0ZnyFcNkBv4zuBWbaeElV4uXK/b3JAoGBAP+vlFaes0vKsUXphfKzSWSUg9SIxr2cAJ9c2t7tjtzTZUiskj61r7fWiyAeta8xCHkdY0CLfKP5v6LfP14fjWK3Q3DCSY9cBEzGmVLBm/vcbefFgJRKU7aFDZ6wCe3e3b4s3ftwaiOYqxIaoACeGgwXHYRFtzW0aksgs18lyWltAoGBAPD+/PdDEd4bsi9l8nVL3h+uUf7ZUOcMNEOyUz8UVtCbpiyrFV8OTFSdscXI93Rm0wa3Ve9wZcyqwDGms9pa4J5zTiq63ae05sch8NYk4Q0KFjDW8TNVOyCZG4uevHJa3ffE7ifztpkicV2caMVt/mjuTMkZQYGu6ZXbReGSo4r/AoGBAIfhutbR3n2ACfgao+oYp/+BAhKYYe5wktAem97vpwXqfqBBvjL/gZQUu7llOK8TQuqC2LV7q9DFMLgRJu8Rm6UDuh6Z0lgS0eIvhVo6tHgEbJBJIQ0t9xE/4r4b1hsJXxTraUlwM6gZQYkMh03st/EG89PQ7Q3ohLjKdykwvrp9AoGBAKkLE0IVp6jWYIxixEmGqA4s5pMOuHL42ohJw57Rk3vMUimu79S3YM9Rter4ZqsdnRRu8TZ87ss7UokBV9LoP/qlAsVyQhxrBh3ULuzm/X15/8rOWm4ZcNoSy4GKHMFR/7TWS/92MjUENeTl24/w8a2EyhOdRZfDq1FUd5Ycl97dAoGBAOVQEx1Q9tyf+zjbdS8+LTAevKWnhjc7I4TkNsryjVLqIr8a6n1WrJBQqDNNgB6UJl2lNkKoUhCaweCYqJsdTSKadaoXwPyJBua6j/zGzIx70kkJ8177T4cQRNe+jEEGGv0hIoZ3hUYBXfLnJehWwlbU5xKfY4NFasRLVU6SL9Zj'
    alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAktBCq9epRgycwl9OildNm3hk2dtlDQc4HjIFdzZb6HJ9AZQ0fYc3OEERls+P2OBXte/Uc1QcYKNOnBvKaoIzHyhC3qx1tXHyPPQvLH7ddsvw48kCLVFbb0fT3g7sVprSTcscOfNQq/diqXnERHafwp0iipqGzdNgiKEetnSqPqWBY/3ATP9eJuz+F4lzOV05NqOCl3AexOZpE0e1mygo+L14XWSdf3WK943uEF+BDyK2J0KJaQRDCoXpZ2yMBN4dOAO0DWmV9M0tk/4gzEQizYVxfzJqMcxaYhOsBIVCHXS6URsx7Gn0XuXI+dPXTVHCFy7Zl1e3qOC6jXsqp5xfCQIDAQAB'
    client = DefaultAlipayClient(alipay_client_config, logger)
    # 构造请求参数对象
    model = AlipayTradePagePayModel()
    model.out_trade_no = str(order_id)
    model.total_amount = str(amount)
    model.subject = str(product_id)
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    # model.buyer_id = "2088722037372474"
    # model.seller_id = "2088721037401832"
    # model.body = "test"
    request = AlipayTradePagePayRequest(biz_model=model)
    request.notify_url = "https://www.baidu.com" #直接跳转
    request.return_url = address #异步
    # 执行API调用

    response = client.page_execute(request, http_method="GET")

    return redirect(response)



def chatMessage(request):#用于对话流的实现,只接受POST
    data = {}
    user = getUser(request)
    engineID = 0
    historyID = -1
    if not user:
        return redirect('/signin') #没有登录态返回到登录页面
    if request.method == 'POST':
        data['status'] = 0
        if not request.content_type == 'application/json':
            return JsonResponse({'error': 'Content-Type must be application/json'}, status=400)

        try:
            # 尝试解析请求体为JSON
            data = json.loads(request.body)
            print(data)
            if data.get('message') is not None:#收到有效消息
                print('收到有效消息:'+data.get('message'))
                message = data.get('message')
                print(data)
                engineID = int(data['engineID'])
                historyID = str(data['historyIndex']) #获得engineID和historyIndex
                promptID = int(data['promptID'])
                data['status'] = 1
        except :
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
        returnContent = {'status':'fail'}
        if data['status']:#收到有效消息：
            returnContent['status'] = 'success'
            #处理消息流
            modelMessage = chat(True,message,promptID,historyID,engineID)
            #
            if modelMessage is None:
                return JsonResponse({'error': 'promptFail'}, status=400)
 
            #modelMessage = '## <h1>返回消息</h1>' #模型返回消息
            returnContent['message'] =markdown.markdown(html.escape(modelMessage)) # 到此说明成功与接口获得信息。接下来将内容存到历史记录
            if historyID == '-1':#如果是新对话
                #创建一个新的对话目录
                engine = aiEngine.objects.get(id=engineID)#获得engine对象

                newChatHistoryIndex = chatHistoryIndex(user=user,title=message[:15],engineID=engine)#用第一条消息作为标题
                newChatHistoryIndex.save()#保存
                historyID=newChatHistoryIndex.id#获得有效的对话Id
                returnContent['historyID']=historyID#返回当前的对话id
                returnContent['chatTitle']=newChatHistoryIndex.title
                userContent = chatHistoryContent(indexID=newChatHistoryIndex,chatContent=message,messageID=0)
                userContent.save()
                modelContent = chatHistoryContent(indexID=newChatHistoryIndex,chatContent=modelMessage,messageID=1,role=True)
                modelContent.save()
            else:
                if  not is_valid_uuid4(historyID):
                    return JsonResponse({'error': 'Invalid history'}, status=400)
                else:
                    curHistoryIndex = chatHistoryIndex.objects.get(id=historyID)
                    curCount = chatHistoryContent.objects.filter(indexID=curHistoryIndex).count()#获得数目
                    returnContent['historyID']=historyID#返回当前的对话id
                    returnContent['chatTitle']=curHistoryIndex.title
                    userContent = chatHistoryContent(indexID=curHistoryIndex,chatContent=message,messageID=curCount)
                    userContent.save()
                    modelContent = chatHistoryContent(indexID=curHistoryIndex,chatContent=modelMessage,messageID=curCount+1,role=True)
                    modelContent.save()

            return JsonResponse(returnContent)
        #input_data = data.get('data', '')

        # 这里可以对输入的数据进行处理，例如保存到数据库、进行计算等
        #processed_data = f"You entered: {input_data}"

        # 返回JSON响应
        return JsonResponse(returnContent)#{'processed_data': processed_data})
    

def clearLogin(request):
    request.session.flush() #清空当前会话缓存
    return redirect('/signin')


