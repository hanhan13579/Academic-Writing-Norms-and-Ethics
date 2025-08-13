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

- 游戏类query调用tools中的`gameTopic`函数；
- 非游戏类query调用tools中的`otherTopic`函数；
- 对没有调用函数的query再进行一次判断，如果第二次没有调用函数，那就既不属于游戏意图也不属于非游戏意图，无需调用函数


"""


def get_response(messages):

    url = "http://10.80.4.142:9527/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    body = {"model": "Qwen3-32B-AWQ", 
            "messages": messages, 
            "tools": tools,
            "stream": False,
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 20,
            "max_tokens": 2048,
            "presence_penalty": 1.5,
            "chat_template_kwargs": {"enable_thinking": False}
            }

    response = requests.post(url, headers=headers, json=body)
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
    
    df = pd.read_excel('d:/项目文件/test.xlsx', header=None, names=['query', 'ground_truth'])

    user_queries = df['query'].tolist()

    ground_truth_map = dict(zip(df['query'], df['ground_truth']))

    batch_process(user_queries, output_filename, prompt)
    print_metrics()