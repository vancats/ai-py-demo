from zhipuai import ZhipuAI
from dotenv import dotenv_values
from typing import List, Dict

config = dotenv_values(".env")
MODEL = 'glm-4-plus'
EXIT_COMMAND = '退出'

class ChatBot:
    def __init__(self, api_key: str, system_message: str = "", model: str = MODEL, exit_command: str = EXIT_COMMAND):
        self.client = ZhipuAI(api_key=api_key)
        self.model = model
        self.exit_command = exit_command
        self.messages: List[Dict[str, str]] = []
        if system_message:
            self.messages.append({"role": "system", "content": system_message})

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_response(self) -> str:
        try:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=self.messages
            )
            answer = response.choices[0].message.content.strip()
            return answer
        except Exception as e:
            return "抱歉，我暂时无法回答这个问题，请稍后再试。错误信息：{e}"

def chat():
    system_message = "用鲁迅的语气和我说话。"
    chatbot = ChatBot(api_key=config['ZHIPUAI_API_KEY'], system_message=system_message)

    print("欢迎使用智能客服对话机器人！输入'退出'以结束对话。")

    while True:
        user_input = input("你：")
        if user_input.strip() == EXIT_COMMAND:
            print("对话已结束。")
            break
        # 获取响应
        chatbot.add_message("user", user_input)
        response = chatbot.get_response()
        print(f"AI：{response}")
        chatbot.add_message("assistant", response)
        print("*" * 50)

chat()
