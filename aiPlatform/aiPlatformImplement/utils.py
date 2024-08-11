from .models import *
import uuid
from .aiEngineAccess import *


def checkLoginByID(id): #使用id检查登录态的方法
    Query_temp = UserAccount.objects.filter(id = id) #执行查询
    if Query_temp.exists():#如果查询到对应的数据
        loginUser = Query_temp.first()#获得当前登录的用户信息
        return loginUser#返回查找到的用户信息
    else: #如果查询不到
        return None#返回none
    
def modifyCredits(user:UserAccount,creditsChange=0,sudo:bool = False):
    #检查UserAccount内的credits情况
    try:
        curCredits = user.user_Credits
        if(curCredits + creditsChange < 0):#余额不足
            if sudo:
                user.user_Credits = curCredits + creditsChange
                return user.user_Credits
            return '余额不足'
        else:
            user.user_Credits = curCredits + creditsChange
            user.save()
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

