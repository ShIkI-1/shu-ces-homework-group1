from .models import *
from django.shortcuts import redirect

def checkLoginByID(id): #使用id检查登录态的方法
    Query_temp = UserAccount.objects.filter(id = id) #执行查询
    if Query_temp.exists():#如果查询到对应的数据
        loginUser = Query_temp.first()#获得当前登录的用户信息
        return loginUser#返回查找到的用户信息
    else: #如果查询不到
        return None#返回none
    
def modifyCredits(user:UserAccount,creditsChange=0,sudo:bool = False,descrip:str = '默认消息'):
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