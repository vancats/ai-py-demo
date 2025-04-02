from zhipuai import ZhipuAI
from dotenv import dotenv_values
import time

config = dotenv_values(".env")
client = ZhipuAI(api_key=config['ZHIPUAI_API_KEY'])

MODEL = 'glm-4-plus'
EXIT_COMMAND = '退出'

stream = client.chat.completions.create(
    model="glm-4-plus",
    messages=[
        {
            "role": "user",
            "content": "有透明的金属吗？",
        }
    ],
    stream=True
)

def process_stream(stream):
    start_time = time.time()
    usage_info = None
    have_received_first_token = False
    try:
        for chunk in stream:
            # 处理内容
          if chunk.choices and chunk.choices[0].delta.content:
            if not have_received_first_token:
                ttft = time.time() - start_time
                have_received_first_token = True

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

        total_time = time.time() - start_time
        print(f"\n接收第一个token的时间: {ttft:.3f}秒", flush=True)
        print(f"接收完整响应的时间: {total_time:.3f}秒", flush=True)
    finally:
        stream.close()

process_stream(stream)
