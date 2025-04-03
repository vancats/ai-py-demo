from zhipuai import ZhipuAI
from dotenv import dotenv_values
import json
import requests
from bs4 import BeautifulSoup

config = dotenv_values(".env")
MODEL = 'glm-4-plus'

article_search_tool = [
    {
        "type": "function",
        "function": {
            "name": "get_article",
            "description": "A tool to retrieve an up to date baidu article, notice, should be English.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "The search term to find a baidu article by title, notice, should be English."
                    }
                },
                "required": ["search_term"]
            }
        }
    }
]

def get_article(search_term):
    url = f"https://baike.baidu.com/item/{search_term}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text()
    print("百度百科的原文：")
    print(text[:500])
    return text if soup else None

def parse_function_call(response, messages: list[dict[str, str]], client: ZhipuAI):
    try:
        if response.choices[0].message.content:
            print('没有返回工具函数')
            messages.append({"role": "assistant", "content": response.choices[0].message.content})
        else:
            print('返回工具函数')
            tool_call = response.choices[0].message.tool_calls[0]
            print("工具函数的名字:",tool_call.function.name)
            print("工具函数的输入:",tool_call.function.arguments)
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            messages.append(response.choices[0].message.model_dump())
            # 定义支持的函数处理逻辑
            function_map = {
                "get_article": get_article
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
            stream=True,
        )
    except Exception as e:
        print(f"Error while parsing function call: {e}")
        return None


def process_stream(stream):
    usage_info = None
    try:
        for chunk in stream:
            # 处理内容
          if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)

            # 检查 usage
            if chunk.usage:
                usage_info = chunk.usage
                if usage_info:
                    print(f"\nPrompt Tokens: {usage_info.prompt_tokens}")
                    print(f"Completion Tokens: {usage_info.completion_tokens}")
                    print(f"Total Tokens: {usage_info.total_tokens}")
                else:
                    print("\n未找到 usage 信息。")

    finally:
        print('传输结束')
        # stream.close()

if __name__ == "__main__":
    client = ZhipuAI(api_key=config['ZHIPUAI_API_KEY'])

    messages = [{"role": "user", "content": "特朗普"}]

    # 传入工具获取工具返回的内容，并且不在 content 而在 tool_calls 中
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=article_search_tool,
        tool_choice="auto"
    )
    # 把返回的数据再传入大模型进行正常的返回
    stream = parse_function_call(response, messages, client)
    process_stream(stream)
