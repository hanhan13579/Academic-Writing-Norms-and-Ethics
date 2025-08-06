import requests
import time
from collections import defaultdict
import pandas as pd

tools = [
    {
                "type": "function",
                "function": {
                    "name": "gameTopic",
                    "description": "判断属于游戏类的问题，使用此function。比如新版本更新了什么内容，游戏模式怎么玩，武器枪支性能评测，角色皮肤相关问题，新手如何上人口，剧场版怎么玩，荣都地图介绍一下等等。",
                    "parameters": {
                        "type": "object",
                        "properties": {

                        }
                    }
                }
            },
    {
                "type": "function",
                "function": {
                    "name": "otherTopic",
                    "description": "判断非游戏类的问题，使用此function。比如锅包肉怎么做，荣耀手机现在卖多少钱，明天冷不冷等等。",
                    "parameters": {
                        "type": "object",
                        "properties": {

                        }
                    }
                }
            },
]



def gameTopic():

    return """ """

def otherTopic():
    
    return """ """


prompt = """
# [任务说明]
你是一个熟悉各类游戏的专家，需要对输入的query进行意图判断，决定调用tools中的哪个函数。

---

## 1：游戏相关问题定义

### 1.1 常见游戏列表
王者荣耀，和平精英，金铲铲之战，火影忍者，暗区突围，三角洲行动，穿越火线-枪战王者…………

### 1.2 用户游戏问题分类
- 新赛季更新内容、改动概要  
- 某个赛季的开始/结束时间、版本内容介绍  
- 上分攻略、宝典，英雄、阵容、吃鸡阵容推荐  
- 角色新老皮肤相关咨询  
- 游戏角色怎么玩  
- 英雄改动  
- 联动IP  
- 新/老地图、不同游戏模型玩法  
- 武器枪支评测、实战打法  
- 天选福星版本玩法  
- 新手攻略、教程（如人口阶段、前期发育、打钱）  
- 新英雄、新忍者、新枪支爆料  
- 版本主题活动奖励、玩法  
- 礼包领取、活动参与、相关攻略

---

## 2：名词提取与判断规则

### 2.1 名词提取
- 判断query中是否包含名词或名词短语  
- 提取所有名词

### 2.2 游戏相关名词判断
- 如果提取的名词中至少有一个属于模块1中的“常见游戏”或“用户游戏问题分类”，则判定为游戏相关；
- “常见游戏”或“用户游戏问题分类”中没显示的不代表不属于游戏分类，需要结合名词具体分析；
- 有时提取的名词属于某个游戏中出现的，这也判定为游戏相关；

### 2.3 特殊名词示例
- “Magic7”（荣耀手机型号）  
- “新干员”（三角洲行动角色）  
- “海岛图”（和平精英地图） 
- “苏尔南冲突”（和平精英一种模式） 
- “王者之击”（穿越火线武器）
…………

---

## 3：特殊情况处理

### 3.1 句式判断
- 出现“在某个[常见游戏]中”的句式时，若后半句内容与游戏无关，判定为非游戏意图

### 3.2 敏感词判断
- 名词中出现敏感词，则既不属于游戏意图也不属于非游戏意图

---

## 4：进一步意图判断

- “你是谁”及相关问题，判定为游戏问题  
- 其余问题判定为非游戏问题

---

## 5：函数调用规则

- 游戏类query调用tools中的`gameTopic`函数；
- 非游戏类query调用tools中的`othertTopic`函数；
- 对没有调用函数的query再进行一次模型2-4的判断，如果第二次没有调用函数，那就既不属于游戏意图也不属于非游戏意图，无需调用函数


---

## 6：回复要求

- 不无中生有  
- 不编造  
- 不进行追问

"""


def get_response(messages):
    api_key = " "
    url = "http://10.71.124.177:8901/v1/chat/completions"
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


call_counts = defaultdict(int)        # function调用次数
correct_call_counts = defaultdict(int) # function正确调用次数
should_call_counts = defaultdict(int)  # function应该调用次数

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
        tool_info["content"] = gameTopic()
    elif assistant_output["tool_calls"][0]["function"]["name"] == "otherTopic":
        tool_info = {"name": "otherTopic", "role": "tool"}
        tool_info["content"] = otherTopic()

    tool_info["duration"] = duration

    
    called_function = None
    if "tool_calls" in assistant_output:
        called_function = assistant_output["tool_calls"][0]["function"]["name"]
        call_counts[called_function] += 1


    expected_function = ground_truth_map.get(user_query, None)
    if expected_function is not None:
        should_call_counts[expected_function] += 1

    if called_function == expected_function and called_function is not None:
        correct_call_counts[called_function] += 1

    return called_function, tool_info["duration"]

def print_metrics():
    total_calls = sum(call_counts.values())
    print("Function调用比例:")
    for func, count in call_counts.items():
        ratio = count / total_calls if total_calls > 0 else 0
        print(f"{func}: {ratio:.2%} ({count}次调用)")

    print("\nFunction准确率和召回率:")
    for func in should_call_counts.keys():
        precision = correct_call_counts[func] / call_counts[func] if call_counts[func] > 0 else 0
        recall = correct_call_counts[func] / should_call_counts[func] if should_call_counts[func] > 0 else 0
        print(f"{func} - 准确率: {precision:.2%}, 召回率: {recall:.2%}")


output_filename = "d:/项目文件/test-result-withoutthink.txt"

def batch_process(user_queries, output_filename, prompt):
    with open(output_filename, "w", encoding="utf-8") as fout:
        for user_query in user_queries:
            result = call_with_messages(user_query, prompt)
            if isinstance(result, tuple) and len(result) == 2:
                name, d = result
                # fout.write(f"Tool: {name}, durations: {d:.2f}\n\n")
                fout.write(name + "\n")
            else:
                fout.write(f"Response: {result}\n")



if __name__ == "__main__":
    
    df = pd.read_excel('d:/项目文件/test_2.xlsx', header=None, names=['query', 'ground_truth'])

    user_queries = df['query'].tolist()

    ground_truth_map = dict(zip(df['query'], df['ground_truth']))

    batch_process(user_queries, output_filename, prompt)
    print_metrics()