import requests
import time
import pandas as pd

tools = [
    {
        "type": "function",
        "function": {
            "name": "gameTopic",
            "description": "query涉及电子游戏的游戏玩法、攻略、角色设定、道具、装备、地图、关卡、电竞赛事等相关内容",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "financeTopic",
            "description": "query涉及金融、投资、理财、经济等相关内容，比如股票、基金、保险、贷款等方面的问题",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lawTopic",
            "description": "query涉及法律、法规、合规、知识产权、合同、诉讼等相关内容",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "telecomTopic",
            "description": "query涉及通信、网络、运营商、资费、套餐、信号等相关内容",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "medicineTopic",
            "description": "query涉及医学、药学、疾病、症状、治疗、健康等相关内容",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "insuranceTopic",
            "description": "query涉及保险、理赔、投保、保单、保险产品等相关内容",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "otherTopic",
            "description": "query不属于gameTopic、financeTopic、lawTopic、telecomTopic、medicineTopic、insuranceTopic中任一分类类别",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
]


prompt = """
# [任务说明]
你是一个专业的通用智能体助手，能够识别query属于如下的哪一类别：

## 一、类别定义：
1. gameTopic：如果query涉及电子游戏的游戏玩法、攻略、角色设定、道具、装备、地图、关卡、电竞赛事等相关内容，则归为“gameTopic”；
2. financeTopic：如果query涉及金融、投资、理财、经济等相关内容，比如股票、基金、保险、贷款等方面的问题，则属于“financeTopic”;
3. lawTopic：如果query涉及法律、法规、合规、知识产权、合同、诉讼等相关内容，则属于“lawTopic”；
4. telecomTopic：如果query涉及通信、网络、运营商、资费、套餐、信号等相关内容，则属于“telecomTopic”；
5. medicineTopic：如果query涉及医学、药学、疾病、症状、治疗、健康等相关内容，则属于“medicineTopic”；
6. insuranceTopic：如果query涉及保险、理赔、投保、保单、保险产品等相关内容，则属于“insuranceTopic”；
7. otherTopic：如果query不属于gameTopic、financeTopic、lawTopic、telecomTopic、medicineTopic、insuranceTopic中任一分类类别，则属于“otherTopic”。


## 二、每个query根据分类类别的定义选择一个合适的类别并输出类别名称。
1. 从类别 1 开始，依次检查 query 是否符合该类别定义；
2. 一旦匹配成功，立即停止判断并输出该类别名称；
3. 如果全部类别都不匹配，则归类为“otherTopic”；

## 三、回复要求：不无中生有、不编造。
"""


def get_response(messages):
    api_key = " "
    url = "http://10.71.125.108:18901/v1/chat/completions"
    headers = {"Content-Type": "application/json", 
               "Authorization": f"Bearer {api_key}"}
    body = {"model": "Qwen3-32B", 
            "messages": messages, 
            "tools": tools,
            "stream": False,
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 20,
            "max_tokens": 32768,
            "presence_penalty": 1.5,
            "chat_template_kwargs": {"enable_thinking": False}
            }

    response = requests.post(url, headers=headers, json=body, proxies={})
    return response.json()


def call_with_messages(user_query, prompt):
    start = time.time()
    messages = [
        {"role": "user", "content": user_query},
        {'role': 'system', 'content': prompt},
    ]

    first_response = get_response(messages)

    
    duration = time.time() - start

    assistant_output = first_response["choices"][0]["message"]
    if assistant_output["content"] is None:
        assistant_output["content"] = ""

    if "tool_calls" not in assistant_output or not assistant_output["tool_calls"]:
        return assistant_output['content']

    if assistant_output["tool_calls"][0]["function"]["name"] == "gameTopic":
        tool_info = {"name": "gameTopic", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "otherTopic":
        tool_info = {"name": "otherTopic", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "生活百科":
        tool_info = {"name": "生活百科", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "健康常识":
        tool_info = {"name": "健康常识", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "地点查询":
        tool_info = {"name": "地点查询", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "影音小说":
        tool_info = {"name": "影音小说", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "天气查询":
        tool_info = {"name": "天气查询", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "菜谱推荐":
        tool_info = {"name": "菜谱推荐", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "金融理财":
        tool_info = {"name": "金融理财", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "产品评价":
        tool_info = {"name": "产品评价", "role": "tool"}
    
    elif assistant_output["tool_calls"][0]["function"]["name"] == "交通服务":
        tool_info = {"name": "交通服务", "role": "tool"}
       
    elif assistant_output["tool_calls"][0]["function"]["name"] == "新闻阅读":
        tool_info = {"name": "新闻阅读", "role": "tool"}
        
    elif assistant_output["tool_calls"][0]["function"]["name"] == "语法词汇":
        tool_info = {"name": "语法词汇", "role": "tool"}
     

    tool_info["duration"] = duration

    return tool_info["name"], tool_info["duration"]


output_filename = "d:/项目文件/test-result-withoutthink.txt"

def batch_process(user_queries, output_filename, prompt):
    with open(output_filename, "w", encoding="utf-8") as fout:
        for user_query in user_queries:
            result = call_with_messages(user_query, prompt)
            if isinstance(result, tuple) and len(result) >= 1:
                name = result[0]
            else:
                name = str(result)
            
            # 如果 name 不是字符串，转成字符串
            if not isinstance(name, str):
                name = str(name)

            # 去掉首尾引号（如果有）
            if name.startswith('"') and name.endswith('"'):
                name = name[1:-1]
            if name.startswith("'") and name.endswith("'"):
                name = name[1:-1]

            fout.write(name + "\n")


if __name__ == "__main__":
    
    df = pd.read_excel('d:/项目文件/11111.xlsx', header=None, names=['query'])

    user_queries = df['query'].tolist()

    batch_process(user_queries, output_filename, prompt)
    