from .models import *
import string
import secrets
from datetime import *

HOSTURL = '127.0.0.1'
import uuid
from .aiEngineAccess import *


def checkLoginByID(id): #使用id检查登录态的方法
    Query_temp = UserAccount.objects.filter(id = id) #执行查询
    if Query_temp.exists():#如果查询到对应的数据
        loginUser = Query_temp.first()#获得当前登录的用户信息
        return loginUser#返回查找到的用户信息
    else: #如果查询不到
        return None#返回none
    
def modifyCredits(user:UserAccount,creditsChange:int=0,sudo:bool = False,descrip:str = '无'):
    #检查UserAccount内的credits情况
    try:
        curCredits = user.user_Credits
        if(curCredits + creditsChange < 0):#余额不足
            if sudo:
                user.user_Credits = curCredits + creditsChange
                user.save() #保存变更
                historyObject = creditHistory(user=user,credits=creditsChange,descriptionText='管理员操作'+descrip)
                historyObject.save()

                order = Order(
                    user=user,
                    product_id="积分变动",
                    amount=creditsChange,
                    status='completed',
                    operation="积分",
                    note='管理员操作'+descrip
                )
                order.save()
                return True
            return False
        else:
            user.user_Credits = curCredits + creditsChange
            user.save()
            historyObject = creditHistory(user=user,credits=creditsChange,descriptionText=descrip)
            historyObject.save()
            # print("充值积分2")
            order = Order(
                user=user,
                product_id="积分变动",
                amount=creditsChange,
                status='completed',
                operation="积分",
                note=descrip
            )
            
            order.save()

            return True

    except Exception as e:
        print("程序有异常，异常信息是：", repr(e))
        print("积分变更错误")
        return False

    
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
    number=int(number)
    try:
        print("充值积分")
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

def checkModelAccess(request,engineID,prompt:ai=None):
    try:
        if engineID == 0:
            return 1
        user = getUser(request)
        engine = aiEngine.objects.get(id = engineID)
        access = ModelAccess.objects.get(user=user,engine=engine)
        if access is None:
            return 0
        if modelAccessExpired(access):#模型未过期
            if (prompt is None) or (checkPromptAccess(user,prompt)):
                return 1
            else:
                return 0
        return 0
    except:
        return 0
            
def grantPromptAccess(user:UserAccount,prompt:ai):#授予prompt权限
    try:
        access = promptAccess.objects.get(user=user,aiPrompt=prompt)
        return 1
    except:
        try:
            access = promptAccess(user=user,aiPrompt=prompt,payed=True)
            access.save()
        except:
            return 0
        return 1 

    
def checkPromptAccess(user:UserAccount,prompt:ai):
    try:
        access = promptAccess.objects.get(user=user,aiPrompt=prompt)
        if access is None:
            return 0
        else:
            return 1
    except:
        return 0
 
           
            
           
def is_valid_uuid4(value):
    print(value)
    try:
        uuid_obj = uuid.UUID(value, version=4)
    except ValueError:
        return False
    return True


def chat(isDebug,content,promptID,historyID,engine):
    #先测试内容是否为空
    if content is None:
        return None
    #再测试promptID
    promptContent = '未使用prompt'
    isPrompt = 0
    if promptID != -1:
        promptContent = str(ai.objects.get(id=int(promptID)).prompt.text)
 
        try:
            promptContent = str(ai.objects.get(id=int(promptID)).prompt.text)
            isPrompt = 1
        except:
            return None
    #测试history
    historyList = []
    isHistory = 0
    if historyID != '-1':
        if historyID is not None and is_valid_uuid4(historyID):
            index = chatHistoryIndex.objects.get(id=historyID) #获得index对象
            if index is not None: #有效
                chatContent = chatHistoryContent.objects.filter(indexID=index).order_by('messageID')
                for i in  chatContent:
                    contentItem = {}
                    contentItem['role'] = i.role
                    contentItem['message'] = i.chatContent#进行md转换
                    historyList.append(contentItem)
                #构造字典
                isHistory = 1

    
    if isDebug:
        return '调试模式，调用数据为:引擎:'+str(engine)+'内容:'+str(content)+'prompt:'+promptContent+'历史'+str(isHistory)
    else:
        return sparkChat(engine,content,isPrompt,promptContent,isHistory,historyList)

def getCredits(user:UserAccount):
    #检查UserAccount内的credits情况
    curCredits = user.user_Credits
    return curCredits