from google import genai
from dotenv import dotenv_values
import requests
from bs4 import BeautifulSoup # type: ignore
from prompt import sanguo_prompt, sanguo_prompt_template

config = dotenv_values(".env")
client = genai.Client(api_key=config['GOOGLE_API_KEY'])
model = 'gemini-2.0-flash'

def fetch_article_content(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  for script in soup(["script", "style"]):
    script.decompose()

  text = soup.get_text()
  # 将文本分割成行，并移除首尾空格
  lines = (line.strip() for line in text.splitlines())
  # 将多个标题分割成单独的行
  chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
  # 移除空行
  text = '\n'.join(chunk for chunk in chunks if chunk)
  # print(f"从书中获取了 {len(text)} 个字符")
  # print("前2000个字符：")
  # print(text[:2000])
  return text

def answer_question(question):
  prompt = sanguo_prompt_template.format(PAPER_CONTENT=book_content, USER_QUESTION=question)
  response = chat.send_message(prompt)
  return response.text

# 德道经
# book_url = "https://www.gutenberg.org/cache/epub/7337/pg7337.txt"
# 三国演义
book_url="https://www.gutenberg.org/cache/epub/23950/pg23950.txt"
book_content = fetch_article_content(book_url)

chat = client.chats.create(model=model, config={
  "system_instruction": sanguo_prompt,
  "safety_settings": [
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_NONE"
    },
  ]
})

response = answer_question("曹操是什么样的人，一些事迹和言语可以体现曹操的个性?")
print(response)
