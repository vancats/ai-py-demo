from google import genai
from dotenv import dotenv_values
from datetime import datetime
from google.genai.types import ModelContent, Part, UserContent, Content
import json

def enhanced_chat_with_gemini(client: genai.Client, model: str, initial_history = list[Content], max_turns=10, save_history=True):
  try:
    if initial_history:
      chat = client.chats.create(model=model, history=initial_history)
      handle_special_commands('/history', chat)
      print('========对话历史========')
    else:
      chat = client.chats.create(model=model, history=None)
      print("开始新的对话。")
  except Exception as e:
    print(f"发生错误: {e}")
    return

  turn_count = 0
  while turn_count < max_turns:
    user_input = input("你: ")
    if user_input.lower() in ['exit', 'quit', 'bye', '退出', '再见']:
      print("结束对话。")
      break

    if user_input.startswith('/'):
      handle_special_commands(user_input, chat)
      continue

    try:
      response = chat.send_message(user_input)
      print(f"Gemini: {response.text}")
    except Exception as e:
      print(f"发生错误: {e}")
      break
    turn_count += 1

  if save_history:
    save_chat_history(chat.get_history())

  return chat.get_history()

def handle_special_commands(command, chat):
  if command == '/clear':
    chat.clear_history()
    print("对话历史已清除。")
  elif command == '/history':
    history = chat.get_history()
    for msg in history:
      role = "User" if msg.role == "user" else "Gemini"
      content = ''.join([part.text for part in msg.parts])
      print(f"{role}: {content}")
  elif command == '/save':
    save_chat_history(chat.get_history())
    print("对话历史已保存。")
  else:
    print("无效命令。")

def save_chat_history(chat_histroy):
  serialized_history = []

  for msg in chat_histroy:
    try:
      content = ''
      for part in msg.parts:
        content += part.text
      # 创建可序列化的字典
      serialized_history.append({
        'role': msg.role,
        'parts': content
      })

    except Exception as e:
      print(f"保存对话历史时发生错误: {e}")

  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  filename = f"chat_history_{timestamp}.json"

  try:
    with open(filename, 'w', encoding='utf-8') as f:
      json.dump(serialized_history, f, ensure_ascii=False, indent=4)
      print(f"对话历史已保存到 {filename}")
  except Exception as e:
    print(f"保存对话历史时发生错误: {e}")

def format_message_history_to_gemini_standard(
    message_history: list[any],
) -> list[Content]:

    converted_messages: list[Content] = []
    for msg in message_history:
        if msg["role"]== "model":
            converted_messages.append(
                ModelContent(parts=[Part(text=msg["parts"])])
            )
        elif msg["role"] == "user":
          converted_messages.append(
              UserContent(parts=[Part(text=msg["parts"])])
          )
    return converted_messages

if __name__ == "__main__":
  config = dotenv_values(".env")
  api_key = config['GOOGLE_API_KEY']

  if not api_key:
    print("未设置 API_KEY")
    exit(1)

  client = genai.Client(api_key=api_key)
  model = 'gemini-2.0-flash'

  with open('chat_history_20250328_215800.json', 'r', encoding='utf-8') as f:
    initial_history = json.load(f)

  initial_history = format_message_history_to_gemini_standard(initial_history)
  enhanced_chat_with_gemini(client, model, initial_history = initial_history)
