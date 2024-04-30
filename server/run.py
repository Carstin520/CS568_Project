import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from instructions import language_teacher_instructions
from functions import translate, speak, set_teaching_language
from dall_e_3 import get_dalle_image
from assistant import create_assistant, create_thread, get_completion


# 创建 FastAPI 实例
app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的来源列表
    allow_credentials=True,
    allow_methods=["*"],  # 允许的方法
    allow_headers=["*"],  # 允许的头部
)

# 定义数据模型
class ChatMessage(BaseModel):
    message: str
    thread_id: str
    
DEBUG = True

# 创建 Assistant
assistant_id = create_assistant(
    name="Language Teacher",
    instructions= language_teacher_instructions,
    model="gpt-4-turbo",
    tools=[
        {
            "type": "retrieval"  # 知识检索
        },
        {
            "type": "code_interpreter"  # 代码解释器
        },{
            "type": "function",  # 用于翻译的函数
            "function": {
                "name": "translate",
                "description": "将文本从源语言翻译为目标语言.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to be translated."
                        },
                        "target_language": {
                            "type": "string",
                            "description": "The target language for the translation."
                        }
                    },
                    "required": ["text", "target_language"]
                }
            }
        },
        {
            "type": "function",  # 用于设置教学语言的函数
            "function": {
                "name": "set_teaching_language",
                "description": "设置教学语言.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "language": {
                            "type": "string",
                            "description": "The language to be taught. And a following learning plan will be generated based on this language."
                        },
                    },
                    "required": ["language"]
                }
            }
        },
        {
            "type": "function",  # 用于将文本转换为语音的函数
            "function": {
                "name": "speak",
                "description": "将文本转换为语音.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to be converted to speech."
                        },
                    },
                    "required": ["text"]
                }
            }
        }
    ],
    files=["../data/knowledge.txt"],
    debug=DEBUG
)

# 创建函数调用列表
funcs = [set_teaching_language, speak]


@app.get("/create_thread")
async def create_thread_endpoint():
    # 创建 Thread
    thread_id = create_thread(debug=DEBUG)
    return {"thread_id": thread_id}

@app.post("/chat")
async def chat_endpoint(request: ChatMessage):
    # 处理请求，返回响应
    message = main(request.message, request.thread_id, debug=DEBUG)
    if isinstance(message, dict) and "image" in message.keys():
        return {
            "message": "",
            "image": message["image"]
        }
    return {
        "message": message,
        "image": ""
    }

def main(query, thread_id, debug=False):
    # 根据输入获取回答
    message = get_completion(assistant_id, thread_id, query, funcs, debug)
    return message


if __name__ == "__main__":
    uvicorn.run(app, port=8000)