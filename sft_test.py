import requests
import time
import pandas as pd

tools = [
    {
        "type": "function",
        "function": {
            "name": "gameTopic",
            "description": "涉及电子游戏及相关领域的内容，包括但不限于：游戏玩法解析、通关攻略、角色设定、技能加点、道具与装备获取、地图与关卡设计、任务与成就系统、游戏版本更新内容、电竞赛事资讯与战队信息、游戏活动与运营公告、玩家社区讨论等。典型场景示例：1. '王者荣耀怎么上分？' 2. '原神圣遗物最佳搭配推荐' 3. '英雄联盟新赛季排位机制解析' 4. '绝地求生枪械配件选择技巧' 5. 'DOTA2 国际邀请赛赛程'。边界说明：不包括桌面游戏（桌游）、体育运动、棋牌类游戏等非电子游戏；不包括游戏行业法律政策（应归类到 lawTopic）；不包括硬件设备性能问题（应归类到 otherTopic）。常见同义表达：电子游戏、视频游戏、单机游戏、主机游戏、网络游戏、手游、端游、电竞。",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "bankTopic",
            "description": "涉及银行、金融、投资、理财、经济等相关内容，包括但不限于：股票、基金、债券、外汇、黄金、加密货币、贷款、利率、存款、金融市场走势、经济指标解读、资产配置建议；典型场景如“今天上证指数走势如何”“基金定投策略有哪些”“美元兑人民币汇率预测”；不包括保险相关问题（应归类到 insuranceTopic）、金融法规政策（应归类到 lawTopic）、虚拟游戏币或道具交易（应归类到 gameTopic）；常见同义表达：股票=股市/股价/股票行情，基金=公募/私募/ETF，外汇=Forex/汇率。",
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
            "description": "涉及法律、法规、合规、知识产权、合同、诉讼等相关内容，包括但不限于：法律条文解读、合同起草与审查、知识产权申请与维权、纠纷调解与诉讼流程、合规管理与风险防控；典型场景如“劳动合同解除条件”“商标注册流程”“知识产权侵权维权方法”；不包括医学、金融、游戏等领域问题（应归类到对应Topic）；常见同义表达：法律=法令/法规/法条，合同=协议/契约，知识产权=专利/商标/著作权。",
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
            "description": "涉及通信、网络、运营商、资费、套餐、信号等相关内容，包括但不限于：移动通信、宽带网络、5G/4G服务、运营商资费与套餐、信号覆盖与优化、网络故障排查；典型场景如“移动套餐资费详情”“宽带断网怎么解决”“5G信号覆盖范围”；不包括硬件设备性能问题（应归类到 otherTopic）、游戏内网络延迟（应归类到 gameTopic）；常见同义表达：通信=电信/通讯，运营商=移动/联通/电信，资费=套餐费/话费。",
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
            "description": "涉及医学、药学、疾病、症状、治疗、健康等相关内容，包括但不限于：疾病诊断与治疗方案、药物使用与副作用、康复与保健、健康饮食与运动建议、体检指标解读；典型场景如“感冒吃什么药好得快”“高血压的治疗方法”“体检报告怎么看”；不包括宠物疾病（应归类到 otherTopic）、医学行业政策法规（应归类到 lawTopic）；常见同义表达：医学=医疗/医药，疾病=病症/病患，药学=药理/药物学。",
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
            "description": "涉及保险及相关业务的内容，包括但不限于：投保、理赔、保单管理、保险产品对比、保险条款解读、险种推荐、保险计划设计；典型场景如“车险怎么买更划算”“健康险理赔需要哪些材料”“人寿保险和意外险的区别”；不包括与投资理财相关的银行金融问题（应归类到 bankTopic）、保险行业法律法规（应归类到 lawTopic）、宠物保险（应归类到 otherTopic）；常见同义表达：健康险=医疗险/重疾险/疾病保险，人寿险=寿险/终身寿险/定期寿险，财产险=车险/家财险/意外险。",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "weatherTopic",
            "description": "涉及天气及气候相关的内容，包括但不限于：实时天气查询、未来天气预报、气温变化、降水情况、风力风向、空气质量、气象灾害预警、穿衣及出行建议；典型场景如“今天北京的天气怎么样”“明天会下雨吗”“空气质量指数是多少”“外出需要带伞吗”；不包括与气候变化政策、环境保护法规相关的问题（应归类到 lawTopic）；常见同义表达：天气=气象、预报=天气预告、空气质量=空气污染指数。",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "travelTopic",
            "description": "涉及旅游及出行相关内容，包括但不限于：旅游景点的营业时间、门票价格、位置、路线与交通方式、最佳游玩时间、游玩时长、玩法与体验；还包括旅游路线规划、目的地推荐、特色美食与文化介绍、当地住宿与交通建议；典型场景如“故宫几点开门”“黄山门票多少钱”“从上海到西湖怎么去”“什么时候去张家界最合适”“在三亚玩几天比较好”“长城怎么玩更有趣”；不包括与旅游行业政策法规相关的问题（应归类到 lawTopic）、与旅游体验评价相关的问题（应归类到 reviewTopic）；常见同义表达：景点=旅游景区/名胜/景区，门票=票价/入园费，路线=行程/线路。",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mathTopic",
            "description": "涉及各类数学题相关内容，包括但不限于：数学题目解析、计算方法、公式推导、几何问题、代数运算、应用题解答、数学思维训练、解题技巧与步骤讲解；还包括数学知识点总结、考试复习建议、常见易错点分析等；典型场景如“如何计算三角形面积”“分数加减法怎么做”“二元一次方程组的解法”“圆的周长公式是什么”“怎样解应用题”“勾股定理的证明”“微积分求导方法”“概率题怎么解”；不包括与数学无关的学科问题（应归类到 otherTopic）；常见同义表达：数学题=算题/习题/练习题，公式=方程式/运算规则，几何=图形/空间图形，代数=代数式/方程，概率=统计/机率。",
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
            "description": "用于兜底分类，包含所有不符合tools列表中其他任一分类条件的query。",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
]

# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "gameTopic",
#             "description": "涉及电子游戏及相关领域的内容，包括但不限于：游戏玩法解析、通关攻略、角色设定、技能加点、道具与装备获取、地图与关卡设计、任务与成就系统、游戏版本更新内容、电竞赛事资讯与战队信息、游戏活动与运营公告、玩家社区讨论等。",
#             "parameters": {
#                 "type": "object",
#                 "properties": {}
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "bankTopic",
#             "description": "涉及银行、金融、投资、理财、经济等相关内容，包括但不限于：股票、基金、债券、外汇、黄金、加密货币、贷款、利率、存款、金融市场走势、经济指标解读、资产配置建议；",
#             "parameters": {
#                 "type": "object",
#                 "properties": {}
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "lawTopic",
#             "description": "涉及法律、法规、合规、知识产权、合同、诉讼等相关内容，包括但不限于：法律条文解读、合同起草与审查、知识产权申请与维权、纠纷调解与诉讼流程、合规管理与风险防控；",
#             "parameters": {
#                 "type": "object",
#                 "properties": {}
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "telecomTopic",
#             "description": "涉及通信、网络、运营商、资费、套餐、信号等相关内容，包括但不限于：移动通信、宽带网络、5G/4G服务、运营商资费与套餐、信号覆盖与优化、网络故障排查；",
#             "parameters": {
#                 "type": "object",
#                 "properties": {}
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "medicineTopic",
#             "description": "涉及医学、药学、疾病、症状、治疗、健康等相关内容，包括但不限于：疾病诊断与治疗方案、药物使用与副作用、康复与保健、健康饮食与运动建议、体检指标解读；",
#             "parameters": {
#                 "type": "object",
#                 "properties": {}
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "insuranceTopic",
#             "description": "涉及保险及相关业务的内容，包括但不限于：投保、理赔、保单管理、保险产品对比、保险条款解读、险种推荐、保险计划设计；",
#             "parameters": {
#                 "type": "object",
#                 "properties": {}
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "weatherTopic",
#             "description": "涉及天气及气候相关的内容，包括但不限于：实时天气查询、未来天气预报、气温变化、降水情况、风力风向、空气质量、气象灾害预警、穿衣及出行建议；",
#             "parameters": {
#                 "type": "object",
#                 "properties": {}
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "travelTopic",
#             "description": "涉及旅游及出行相关内容，包括但不限于：旅游景点的营业时间、门票价格、位置、路线与交通方式、最佳游玩时间、游玩时长、玩法与体验；还包括旅游路线规划、目的地推荐、特色美食与文化介绍、当地住宿与交通建议；",
#             "parameters": {
#                 "type": "object",
#                 "properties": {}
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "mathTopic",
#             "description": "涉及各类数学题相关内容，包括但不限于：数学题目解析、计算方法、公式推导、几何问题、代数运算、应用题解答、数学思维训练、解题技巧与步骤讲解；还包括数学知识点总结、考试复习建议、常见易错点分析等；",
#             "parameters": {
#                 "type": "object",
#                 "properties": {}
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "otherTopic",
#             "description": "用于兜底分类，包含所有不符合tools列表中其他任一分类条件的query。",
#             "parameters": {
#                 "type": "object",
#                 "properties": {}
#             }
#         }
#     },
# ]


prompt = """
<|im_start|>system\n
你是一个专业的通用智能体助手。具备如下能力：\n
1. 能够根据用户指令，编排生成工具，调用工具的话按照如下格式输出:[{'name': 工具名称, 'arguments': {工具参数名1:工具参数值1, 工具参数名2:工具参数值2}}]。其中每个任务的第一项是工具名称；第二项是工具参数和对应值，不需要输出无关内容。\n
2. 如果你需要调用工具中含有的非必需参数，且非必需参数的参数值无法获取，则在调用该工具时不要传入该参数。\n
3. 如果没有合适工具可以调用，请输出[{'name': otherTopic, 'arguments': {}}]。\n
4. 输出的工具名称必须是tools列表里function名称中的其中一个。\n
5. 不要输出模型对query的直接回答，只需要输出函数调用：[{'name': 工具名称, 'arguments': {}}]。\n\n
You are provided with function signatures within <tools></tools> XML tags:\n
# <tools>\n\n
</tools>\n
<|im_end|>\n\n
<|im_start|>user\n
{user_query}\n
<|im_end|>\n\n
<|im_start|>assistant\n
"""


def get_response(messages):

    url = "http://10.80.4.142:9527/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    body = {"model": "Qwen3-8B", 
            "messages": messages, 
            "tools": tools,
            "stream": False,
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 20,
            "max_tokens": 4096,
            "presence_penalty": 1.5,
            "chat_template_kwargs": {"enable_thinking": False}
            }

    response = requests.post(url, headers=headers, json=body)
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

    elif assistant_output["tool_calls"][0]["function"]["name"] == "bankTopic":
        tool_info = {"name": "bankTopic", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "lawTopic":
        tool_info = {"name": "lawTopic", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "telecomTopic":
        tool_info = {"name": "telecomTopic", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "medicineTopic":
        tool_info = {"name": "medicineTopic", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "insuranceTopic":
        tool_info = {"name": "insuranceTopic", "role": "tool"}
    
    elif assistant_output["tool_calls"][0]["function"]["name"] == "weatherTopic":
        tool_info = {"name": "weatherTopic", "role": "tool"}
    
    elif assistant_output["tool_calls"][0]["function"]["name"] == "travelTopic":
        tool_info = {"name": "travelTopic", "role": "tool"}

    elif assistant_output["tool_calls"][0]["function"]["name"] == "mathTopic":
        tool_info = {"name": "mathTopic", "role": "tool"}


    tool_info["duration"] = duration

    return tool_info["name"], tool_info["duration"]


output_filename = "d:/项目文件/test-result-withoutthink.xlsx"

def batch_process(user_queries, output_filename, prompt):
    results = []
    # with open(output_filename, "w", encoding="utf-8") as fout:
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

        # fout.write(name + "\n")
        results.append(name)

    # 保存到 Excel（输入和输出一一对应）
    df_result = pd.DataFrame({
        "输入": user_queries,
        "输出": results
    })
    df_result.to_excel(output_filename, index=False)


if __name__ == "__main__":
    
    df = pd.read_excel('D:/优化实验/test/test_all无分类.xlsx', header=None, names=['query'])

    user_queries = df['query'].tolist()

    batch_process(user_queries, output_filename, prompt)