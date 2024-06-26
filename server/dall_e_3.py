import os
import io
import time
import base64
import matplotlib.pyplot as plt
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv
import requests



# 加载环境变量
load_dotenv()

# 获取 API 密钥
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def base64_to_img(b64_string):
    """
    Convert a base64 encoded string to an image.

    Parameters:
        b64_string (str): The base64 encoded string representing the image.

    Returns:
        Image: The image object.
    """
    img_data = base64.b64decode(b64_string)
    img = Image.open(io.BytesIO(img_data))
    return img


# 获取 dall-e-3 生成的图片
def get_dalle_image(prompt):
    """
    Generate an image based on a given prompt using the DALL-E model.

    Parameters:
    - prompt (str): The prompt for generating the image.

    Returns:
    - img_file_path (str): The file path of the generated image.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    # 获取当前时间戳
    timestamp = int(time.time())
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        # Assuming there's a way to set a timeout in the API call
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            quality="hd",
            size="1792x1024",
            response_format='b64_json',
            timeout=30  # Timeout in seconds
        )
        # ... rest of your code ...
    except requests.Timeout:
        print("Request timed out")
        # Handle timeout
    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle other exceptions
    img_b64 = response.data[0].b64_json
    # 保存图片
    img_name = f"{timestamp}.png"
    img_file_path = f"../web/public/imgs/{img_name}"
    with open(img_file_path, "wb") as f:
        f.write(base64.b64decode(img_b64))
    # 绘制图片
    imgs = base64_to_img(img_b64)
    plt.imshow(imgs)
    plt.axis('off')
    plt.show()
    return {"image": "/imgs/" + img_name}
    

if __name__ == "__main__":
    get_dalle_image("A English teacher teaching a student how to speak English.")