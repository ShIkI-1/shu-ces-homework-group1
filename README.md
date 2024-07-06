# 对接文档
## 涉及到模块交互写这里
### Ai引擎访问模块：
通过 使用prompt 转入使用引擎时，请通过GET方式向我的url传递一个可以唯一标示prompt数据的标识符。
使用方法：href地址设置为`"/chat?engine=0&promptID=123445"`
其中，`engine`范围为0-3，对应max,lite,pro,4.0四种模型；`promptID`为一个能够唯一标识prompt内容的ID字段，请由调用者说明对应数据库字段或实现传入参数为promptID的函数接口用于返回prompt文本

### 用户登陆态获取:`getUser(request)`:
直接传入`request`对象，该函数会自动解析用户id 返回用户对象
成功返回用户对象
失败返回`None`
老接口不会弃用，但是不再推荐使用

### 用户积分获取与变更：
  `modifyCredits(user:UserAccount,creditsChange,sudo:bool = False):`

传入用户对象。调用成功返回用户剩余`credits`。失败返回`None`,操作后余额小于零且非超级操作（`sudo=False`)则不进行操作并返回字符串类型‘余额不足’；操作后余额小于零且为超级操作则会正常将数字降低到0以下并返回余额。获取金额请令`creditsChange`参数为0或留空
消费积分请传入负值，增加传入正值

创建订单的方式：/order/api/create_order/?product_id=商品名称&amount=金额
