from google import genai
from dotenv import dotenv_values
import pprint

config = dotenv_values(".env")
client = genai.Client(api_key=config['GOOGLE_API_KEY'])
model = 'gemini-2.0-flash'

# 上传文件
# sample_file = client.files.upload(
#     file="images/3.webp",
#     config={"display_name": "Sample drawing"},
# )
# print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

# 列出文件
# for file_path in client.files.list():
#     pprint.pprint(file_path.display_name)

# 模型
# for model in client.models.list():
#     pprint.pprint(model.name)
# model = client.models.get(model='gemini-1.5-flash')
# print(model)

# 生成内容
# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents="Hello!",
# )
# pprint.pprint(response.text)

def chat_with_gemini():
  conversation = []

  while True:
    user_input = input("你: ")

    if user_input.lower() == "exit":
        print("结束对话。")
        print(conversation)
        break

    conversation.append({
      "role": "user",
      "parts": [{"text": user_input}]
    })

    response = client.models.generate_content(
      model=model,
      contents=conversation
    )

    # 打印模型响应
    print(f"Gemini: {response.text}")

    conversation.append({
      "role": "model",
      "parts": [{"text": response.text}]
    })

  return conversation


# history_message = chat_with_gemini()
# print(history_message)


chat = client.chats.create(model=model)
def chat_with_gemini2():

  while True:
    user_input = input("你: ")
    response = chat.send_message(message=user_input)
    print(f"Gemini: {response.text}")
    if user_input.lower() == "exit": break

chat_with_gemini2()
