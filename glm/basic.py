from zhipuai import ZhipuAI
from dotenv import dotenv_values

config = dotenv_values(".env")
client = ZhipuAI(api_key=config['ZHIPUAI_API_KEY'])

MODEL = 'glm-4-plus'
EXIT_COMMAND = '退出'

messages = []
# 设置系统消息
system_message = "用幽默的语气说话"
if system_message:
    messages.append({"role": "system", "content": system_message})

def get_response(user_input):
    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stop=["\n\n"]
        )
        answer = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": answer})
        return answer
    except Exception as e:
        return "抱歉，我暂时无法回答这个问题。"

def chat():
    print("欢迎使用智能客服对话机器人！输入'退出'以结束对话。")

    while True:
        user_input = input("你：")
        if user_input.strip() == EXIT_COMMAND:
            print("对话已结束。")
            break
        # 获取响应
        response = get_response(user_input)
        print(f"AI：{response}")
        print("*" * 50)

chat()
