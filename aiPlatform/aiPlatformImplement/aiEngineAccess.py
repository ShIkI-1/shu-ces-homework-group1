#本文件用于实现ai引擎的访问能力
#本文件可以单独测试
import requests
import markdown
from .sparkConfig import SPARKAI_API_KEY,SPARKAI_APP_ID,SPARKAI_API_SECRET

#星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
#[max,lite,pro,ultra] 
SPARKAI_URL = ['wss://spark-api.xf-yun.com/v3.5/chat','wss://spark-api.xf-yun.com/v1.1/chat','wss://spark-api.xf-yun.com/v3.1/chat','wss://spark-api.xf-yun.com/v4.0/chat']#[max,lite,pro,ultra] 


#星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = ['generalv3.5','general','generalv3','4.0Ultra']




def sparkChat(i:int,content="你好",isPrompt = 0,prompt="你现在是一个大模型",isHistory = 0,history=[{"role":"user","content":"你好"}]):
    if i<0 or i>3:
        return "模型选择错误"
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    if i == 1:
        data = {
        "model": SPARKAI_DOMAIN[i],# 指定请求的模型
        "max_tokens":1024,#最大长度
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    }
    else:
        data = {
                "model": SPARKAI_DOMAIN[i],# 指定请求的模型
                "temperature":0.5,#随机性
                "max_tokens":1024,#最大长度
                "top_k":4,#稳定性
        }
        if isPrompt:#使用prompt的情形
            if isHistory:#使用历史记录的情形
                if len(history) > 7:
                    history = history[-7:]#历史记录只切片7条对话
                data["messages"]= [
                    {
                        "role": "system",
                        "content": prompt
                    }]+history+[
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            else:#不使用历史记录的情形
                data["messages"]= [
                        {
                            "role": "system",
                            "content": prompt
                        },
                        {
                            "role": "user",
                            "content": content
                        }
                    ]
        else:#不使用prompt的情形
            if isHistory:#使用历史记录的情形
                if len(history) > 7:
                    history = history[-7:]#历史记录只切片7条对话
                data["messages"]= history+[
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            else:#不使用历史记录的情形
                data["messages"]= [
                        {
                            "role": "user",
                            "content": content
                        }
                    ]
    header = {
        "Authorization": "Bearer "+SPARKAI_API_KEY+":"+SPARKAI_API_SECRET #认证
    }
    response = requests.post(url, headers=header, json=data)
    if response.status_code == 200:
        response = response.json()
    else:
        returnText = {"code":response.status_code}
        return returnText
    #example = {"code":0,"message":"Success","sid":"cha000b8a53@dx19063e2460eb8f2532","choices":[{"message":{"role":"assistant","content":"您好，我是科大讯飞研发的认知智能大模型，我的名字叫讯飞星 火认知大模型。我可以和人类进行自然交流，解答问题，高效完成各领域认知智能需求。"},"index":0}],"usage":{"prompt_tokens":2,"completion_tokens":40,"total_tokens":42}}
    if response["code"] == 0:
        
        returnText = {"content":response["choices"][0]["message"]["content"],"code":response["code"]}
    else:
        returnText = {"code":response["code"]}

    return returnText



if __name__ == '__main__':
    inputText = input()
    print(sparkChat(2,content=inputText))
    # text = '在Python中，可以使用切片操作来获取数组的后4项。具体代码如下：\n\n```python\narr = [1, 2, 3, 4, 5, 6, 7, 8, 9]\nlast_four_items = arr[-4:]\nprint(last_four_items)\n```\n\n这段代码会输出数组`arr`的后4项，即`[5, 6, 7, 8]`。'
    # html = markdown.markdown(text)
    # print(html.replace("\n","</br>"))