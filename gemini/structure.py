from google import genai
from dotenv import dotenv_values
from typing_extensions import TypedDict
import json
import enum

config = dotenv_values(".env")
client = genai.Client(api_key=config['GOOGLE_API_KEY'])
model = 'gemini-2.0-flash'

class QAPair(TypedDict):
  question: str
  answer: str

schema = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "answer": {"type": "string"}
    },
    "required": ["question", "answer"]
}

chat = client.chats.create(model=model, config={
  "response_mime_type": "application/json",
  # "response_schema": list[QAPair]
  "response_schema": schema
})

# response = chat.send_message("列出几个关于LLM大模型应用开发的常见问题及其答案。")

# response = chat.send_message(
#     "我尝到了一种奇特的水果,它有着粘稠的质地,但却散发着淡淡的甜香。这种食材最可能是什么?",
#     config={
#         "response_mime_type": "application/json",
#         "response_schema": {
#           "type": "STRING",
#           "enum": ["海胆", "榴莲", "臭豆腐", "松露", "鱼子酱"],
#         },
#     },
# )

class Difficulty(enum.Enum):
    SUPER_EASY = "超级简单"
    EASY = "简单"
    MEDIUM = "中等"
    HARD = "困难"
    EXPERT = "专家级"

class CocktailRecipe(TypedDict):
    recipe_name: str
    difficulty: Difficulty
    ingredients: list[str]
    instructions: list[str]

response = chat.send_message(
    """列出约10种鸡尾酒,并提供以下信息:
    1. 鸡尾酒名称
    2. 制作难度评级
    3. 配料清单
    4. 制作步骤
    请包括一些独特或经典的组合。以JSON格式返回结果。""",
    config={
      "response_mime_type": "application/json",
      "response_schema": list[CocktailRecipe]
    }
)

data = json.loads(response.text)
pretty_json = json.dumps(data, indent=4, ensure_ascii=False)
print(pretty_json)
