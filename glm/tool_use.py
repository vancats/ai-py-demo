from zhipuai import ZhipuAI
from dotenv import dotenv_values
import json

config = dotenv_values(".env")
MODEL = 'glm-4-plus'

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "根据城市名称获取当前天气信息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "description": "城市名称,例如:北京",
                        "type": "string"
                    },
                    "date": {
                        "description": "日期,可选,格式为 YYYY-MM-DD",
                        "type": "string"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

def get_weather(city):
    """
    正式业务场景会请求一些实时API得到相关的结果
    """
    return {
        "city": city,
        "date": "明天",
        "temperature": 22,
        "weather": "小雨",
        "humidity": 85,
        "wind": "东北风3级"
    }

def parse_function_call(response, messages, client):
    try:
        tool_call = response.choices[0].message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        messages.append(response.choices[0].message.model_dump())
        # 定义支持的函数处理逻辑
        function_map = {
            "get_weather": get_weather
        }
        if function_name in function_map:
            result = function_map[function_name](**arguments)
            messages.append({
                "role": "tool",
                "content": json.dumps(result, ensure_ascii=False),
                "tool_call_id": tool_call.id
            })

            # 再次调用模型
            return client.chat.completions.create(
                model=MODEL,
                messages=messages,
            )
        else:
            raise ValueError(f"Unsupported function: {function_name}")
    except Exception as e:
        print(f"Error while parsing function call: {e}")
        return None


if __name__ == "__main__":
    client = ZhipuAI(api_key=config['ZHIPUAI_API_KEY'])

    messages = [{"role": "user", "content": "请告诉我北京的天气如何?"}]
    new_message = {"role": "system", "content": "根据天气信息，请你根据现实准确专业的给出出行，穿衣，活动建议"}
    messages.insert(0, new_message)

    # 传入工具获取工具返回的内容，并且不在 content 而在 tool_calls 中
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    # 把返回的数据再传入大模型进行正常的返回
    response = parse_function_call(response, messages, client)
    print(response.choices[0].message.content)
