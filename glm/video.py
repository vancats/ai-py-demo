from zhipuai import ZhipuAI
from dotenv import dotenv_values
import time
import base64

config = dotenv_values(".env")
client = ZhipuAI(api_key=config['ZHIPUAI_API_KEY'])

MODEL = 'CogVideoX-Flash'

response = client.videos.generations(
    model=MODEL,
    # 官方推荐：(镜头语言 + 景别角度 + 光影) + 主体 (主体描述) + 主体运动 + 场景 (场景描述) + (氛围)
    prompt="星空的线条在动",
    image_url="https://cdn.bigmodel.cn/static/platform/images/usage-guide/cogvideo/1.png",
)

task_id = response.id
print(f"任务已提交，任务 ID：{task_id}")

while True:
    result = client.videos.retrieve_videos_result(id=task_id)
    if result.task_status == "SUCCESS":
        video_url = result.video_result[0].url
        cover_image_url = result.video_result[0].cover_image_url
        print(f"视频生成成功！\n视频地址：{video_url}\n封面地址：{cover_image_url}")
        break
    elif result.task_status == "FAIL":
        print(f"视频生成失败")
        break
    else:
        print(f"视频生成中，当前状态：{result.task_status}")
        time.sleep(5)


# /没成功
# Base64 编码
# video_path = "/Users/vancats/Desktop/Demo/ai-py-demo/images/photo.webp"
# with open(video_path, 'rb') as video_file:
#     image_base = base64.b64encode(video_file.read()).decode('utf-8')

# print(image_base)
# response = client.chat.completions.create(
#     model=MODEL,  # 填写需要调用的模型名称
#     messages=[
#       {
#         "role": "user",
#         "content": [
#           {
#             "type": "image_url",
#             "video_url": {
#                 "url" : image_base
#             }
#           },
#           {
#             "type": "text",
#             "text": "请仔细描述这个视频"
#           }
#         ]
#       }
#     ]
# )
# print(response.choices[0].message)
