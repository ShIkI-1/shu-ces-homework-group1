from .models import *
import string
import secrets
from datetime import *

HOSTURL = '127.0.0.1'

def checkLoginByID(id): #使用id检查登录态的方法
    Query_temp = UserAccount.objects.filter(id = id) #执行查询
    if Query_temp.exists():#如果查询到对应的数据
        loginUser = Query_temp.first()#获得当前登录的用户信息
        return loginUser#返回查找到的用户信息
    else: #如果查询不到
        return None#返回none
    
def modifyCredits(user:UserAccount,creditsChange:int=0,sudo:bool = False,descrip:str = '默认消息'):
    #检查UserAccount内的credits情况
    try:
        curCredits = user.user_Credits
        if(curCredits + creditsChange < 0):#余额不足
            if sudo:
                user.user_Credits = curCredits + creditsChange
                user.save() #保存变更
                historyObject = creditHistory(user=user,credits=creditsChange,descriptionText='管理员操作'+descrip)
                historyObject.save()
                return user.user_Credits
            return '余额不足'
        else:
            user.user_Credits = curCredits + creditsChange
            user.save()
            historyObject = creditHistory(user=user,credits=creditsChange,descriptionText=descrip)
            historyObject.save()
            return user.user_Credits
    except:
        return None

    
def getUser(request):
    if request.session.get("id") is not None:
        id = request.session["id"]#另存id
        user = checkLoginByID(id)
        if user is not None:#如果存在登录的用户
            return user
        else :
            request.session.flush() #清空当前会话缓存
            return None
    else:
        return None
    
def generate_token(length=20):
    # 生成包含大小写字母和数字的随机字符串
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    return token

def creditsSettlement(user:UserAccount,number,price):#结算积分购买
    #尝试变更用户积分
    try:
        modifyCredits(user,number,False,'充值积分')
        
    except:
        buyHistory = creditBuyHistory(user=user,credits=number,payed=True,price=price,settled=False)#添加未发放的购买记录
        buyHistory.save()
        return -1
    buyHistory = creditBuyHistory(user=user,credits=number,payed=True,price=price,settled=True)
    buyHistory.save()
    return 1
    
def modelAccessExpired(modelAccess:ModelAccess,time:int=0):#检查访问是否过期,并增加访问天数
    if modelAccess.expireTime > timezone.now(): #检查过期
        if time != 0:#非仅校验
            modelAccess.expireTime = modelAccess.expireTime + timedelta(days=time)
            modelAccess.save()#处理时间
        return 1
    else:   
        if time != 0:#非仅校验
            modelAccess.expireTime = timezone.now() + timedelta(days=time)
            modelAccess.save()#处理时间
        return 0
    pass

def grantModelAccess(user:UserAccount,number:int,engine:aiEngine):#授予用户模型访问权限
    try:
        #先查询有没有存在的访问
        accesses = ModelAccess.objects.get(user=user,engine=engine)
        #如果没有，创建
        if accesses is None:
            accesses = ModelAccess(user=user,engine=engine,payed=True)#创建一个今天过期的内容
            accesses.save()#保存
        #检查是否已经过期,并添加访问权限
        modelAccessExpired(accesses,number)
        return 1
        pass
    except:
        return 0
        pass

def checkModelAccess(request,engineID):
    try:
        user = getUser(request)
        engine = aiEngine.objects.get(id = engineID)
        access = ModelAccess.objects.get(user=user,engine=engine)
        if access is None:
            return 0
        if modelAccessExpired(access):
            return 1
        return 0
    except:
        return 0
            
           
            
           