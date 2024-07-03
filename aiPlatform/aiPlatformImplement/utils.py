from .models import *

def checkLoginByID(id): #使用id检查登录态的方法
    Query_temp = UserAccount.objects.filter(id = id) #执行查询
    if Query_temp.exists():#如果查询到对应的数据
        loginUser = Query_temp.first()#获得当前登录的用户信息
        return loginUser#返回查找到的用户信息
    else: #如果查询不到
        return None#返回none