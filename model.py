import getpass
import os
import json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model

# if not os.environ.get("GOOGLE_API_KEY"):
#   os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
# model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
# model.bind(response_format={"type": "json_object"})

# resp = model.invoke(messages)
# print(resp.content)
# json_response = json.loads(resp.content.replace('json', ''))
# print(json_response)

class LcModel:
    def __init__(self):
        if not os.environ.get("GOOGLE_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
        model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
        model.bind(response_format={"type": "json_object"})

    def genPlan(self, input: str):
        sys_template = """你用户会和你说他想要学习的科目或技能，
            然后你按照初级、中级、高级或者大师级，这三到四个章节为用户规划好每个阶段要学习什么内容，
            相当于共用三到四个章节，每个章节有5-10节, 
            其次，你要判断用户输入的内容是否为不合法课的科目，
            不合法的科目包括比如用户输入的内容不是学科，技能或者技术，比如用户输入了土豆或者你好，这是不合法的科目
            不合法的科目还包括特别大的学科或者特别模糊的技能，因为我们只负责用三到四章让学生快速的了解或者学习某个中小领域的知识，
            比如用户输入了数学、哲学、物理、化学，这种三到四章无法传授的学科要帮学生细化一下领域
            比如心理学是不合法的学科，但是拉康思想是合法，这一点你要自行判断。

            对于合法的学科，直接输出目录，不输出其他内容。
            输出内容是json格式，格式为{"invalid": false, "lesson": [["..."], ["..."],  ["..."],  ["..."]]},如果非法科目的话返回{"invalid": true}
            """

        messages = [SystemMessage(sys_template),HumanMessage(input)]
        plan = self.talkToModel(messages)
        return plan

    def genLesson(input: str):
        pass

    def genTest(input: str):
        pass

    def talkToModel(messages: list) -> dict:
        resp = model.invoke(messages)
        return json.loads(resp.content.replace('json', ''))