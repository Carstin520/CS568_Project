import os
import datetime
import json
import random
import requests
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 获取 API 密钥
NINJAS_API_KEY = os.getenv("NINJAS_API_KEY")

# 获取 API 密钥
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 实例化 OpenAI 客户端
client = OpenAI(api_key=OPENAI_API_KEY, timeout=600)

random.seed(2023)

def translate(text, target_language):
    """
    Translates the given text from the source language to the target language.

    Args:
        text (str): The text to be translated.
        source_language (str): The source language of the text.
        target_language (str): The target language for the translation.

    Returns:
        str: The translated text.
    """
    prompt = f"""
    translate the following text to {target_language}
    Text: {text}
    Only give me the translated text.
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()
    
def speak(text, gender = "man"):
    """
    Using the OpenAI API, this function converts the given text to speech and saves it as an MP3 file.

    Args:
        text (str): The text to be converted to speech.
        gender (str, optional): gender. Defaults to "man".

    Returns:
        file: mp3 file
    """
    
    sound = "echo"
    if gender == "woman":
        sound = "alloy"
        
    response = client.audio.speech.create(
        model="tts-1",
        voice=sound,
        input=text,
    )

    return response.stream_to_file("output.mp3")
    

def set_teaching_language(language, context= "Conversational"):
    """
    Sets the teaching language for the language teacher. Given the language, use openai GPT client to generate a learning plan.

    Args:
        language (str): The language to be taught.
        context (str): The context of the learning plan. Defaults to "Conversational".

    Returns:
        plan(str): a learning plan
    """
    prompt = f"""
    Generate a one time course learning plan for teaching {language} under this following context using chat AI chatbot.
    
    Context: {context}
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0
    )
    plan = response.choices[0].message.content.strip()
    
    with open(f"../data/learning_plan_{language}.txt", "w") as file:
        file.write(plan)
        
    return plan

def check_learning_plan(language):
    """
    Checks the learning plan for a specific language.

    Args:
        language (str): The language to check the learning plan for.

    Returns:
        str: The learning plan for the specified language.
    """
    with open(f"../data/learning_plan_{language}.txt", "r") as file:
        return file.read()
    

        
if __name__ == "__main__":
    print(set_teaching_language("Spanish"))
