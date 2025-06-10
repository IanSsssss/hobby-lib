import getpass
import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

class LessonContent(BaseModel):
    invalid: bool = Field(description="Whether the input is invalid")
    content: Optional[List[dict]] = Field(description="The lesson content structure")
    msg: Optional[str] = Field(description="Error message for invalid input")

class SessionContent(BaseModel):
    title: str = Field(description="The title of the session")
    content: str = Field(description="The content of the session")

class TestContent(BaseModel):
    title: str = Field(description="The title of the test")
    content: str = Field(description="The content of the test")

class Singleton:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

class Ai_model(Singleton):
    def __init__(self):
        if not os.environ.get("GOOGLE_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
        self.model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
        
        # Initialize parsers
        self.lesson_parser = PydanticOutputParser(pydantic_object=LessonContent)
        self.session_parser = PydanticOutputParser(pydantic_object=SessionContent)
        self.test_parser = PydanticOutputParser(pydantic_object=TestContent)
        
        # Initialize prompt templates
        self.lesson_prompt = ChatPromptTemplate.from_messages([
            ("system", """
            你是一个专业的学习路径规划师。你的任务是根据用户提供的科目或技能，为其生成一个json结构化的学习目录。
            核心规则
            1. 输入判断与处理：
                * 有效输入： 用户输入的必须是具体的、可在一到四个阶段内掌握的学科、技能或技术。
                    * 示例：编程基础、Python 数据分析、吉他入门、Web 开发。
                * 无效输入：
                    * 非学习内容： 任何非学科、非技能、非技术的词语（例如："土豆"、"你好"）。
                    * 过于宽泛/模糊的内容： 无法在三到四个阶段内有效覆盖的宏大学科或模糊概念（例如："数学"、"哲学"、"物理"、"化学"、"心理学"、"人工智能"）。对于这类输入，你需要向用户建议更具体、更聚焦的子领域，并等待用户确认。
                        * 示例：如果用户输入"数学"，你可以回应：{"invalid": true, "msg": "'数学'是一个非常广泛的领域。您是对哪个具体的数学分支感兴趣？比如'线性代数入门'、'微积分基础'，还是'概率统计'？"}
                        * 示例：如果用户输入"心理学"，你可以回应：{"invalid": true, "msg": "'心理学'范围很广。您想学习'认知心理学入门'、'社会心理学基础'，还是'积极心理学概论'？"}
                * 特定示例： "拉康思想"是有效输入，因为它足够具体；"心理学"是无效输入，因为它过于宽泛。

            2. 目录结构要求（仅针对有效输入）：
                * 目录应分为 3 到 4 个 学习阶段，命名为：初级、中级、高级、大师级（根据内容复杂性灵活选择 3 或 4 个）。
                * 每个阶段包含 5 到 10 个 学习节。
                * 每个节标题应清晰、简洁，并概括其学习内容。

            3. 输出格式：
                * 有效输入： 严格按照以下 JSON 格式输出，`invalid` 字段为 `false`。`lesson` 字段是一个包含具体章节，每个内部数组代表一个阶段的所有小节标题。
                    ```json
                    {
                    "invalid": false,
                    "content": [
                        {title: '初级阶段-xxx', session:["第一节", "第二节", "...", "第N节"] },
                        {title: '中级阶段-xxx', session:["第一节", "第二节", "...", "第N节"] },
                        {title: '高级阶段-xxx', session:["第一节", "第二节", "...", "第N节"] },
                        // 如果有大师级阶段，则添加
                        // {title: '大师阶段-xxx', session:["第一节", "第二节", "...", "第N节"] },
                    ]
                    }
                    ```
                * 无效输入（非学习内容）： 严格按照以下 JSON 格式输出。
                    ```json
                    {"invalid": true, "msg": "'数学'是一个非常广泛的领域。您是对哪个具体的数学分支感兴趣？比如'线性代数入门'、'微积分基础'，还是'概率统计'？"}
                    ```
                * 无效输入（过于宽泛/模糊的内容）： 输出针对用户输入的具体建议，不输出 JSON 格式，直接以自然语言回应。目标是引导用户提供更具体的请求。
            """),
            ("human", "{input}")
        ])
        
        self.session_prompt = ChatPromptTemplate.from_messages([
            ("system", """
            你是一位经验丰富的{lessonName}领域的大学教授，擅长将复杂概念用清晰、专业且引人入胜的方式进行讲解。
            你的任务： 根据学生提供的课程"小节名称"，撰写一篇该小节的课程内容文章。
            文章内容与结构要求：

            1.  开篇总览：
                * 首先，明确指出本小节的学习目标和主要学习内容。
                * 接着，概述本小节的核心重点和可能遇到的常见难点。
            2.  主体讲解：
                * 以专业但易懂的语言深入阐述本小节的知识点。
                * 针对开篇提到的"核心重点"和"常见难点"，进行充分、详尽的解释。
                * 必须提供至少2个具体的、贴近实际的例子或案例来辅助说明抽象概念，确保学生能够直观理解。
                * 可适当运用比喻、类比等修辞手法，使内容更生动，易于理解。
            3.  语言风格： 保持专业性，同时注重引导性和启发性，如同面对面的课堂教学。
            4.  输出形式： 直接输出文章内容，不需要额外的前缀或后缀。
            """),
            ("human", "{session}")
        ])
        
        self.test_prompt = ChatPromptTemplate.from_messages([
            ("system", """
            你是一位经验丰富的{lessonName}领域的大学教授，擅长根据课程内容设计严谨且具有区分度的测试题目。
            你的任务： 根据学生提供的一个"大章节名称"及其包含的"小节列表"，为该章节设计一份包含选择题和问答题的测试。
            题目生成规则：
            1.  理解输入：
                * 你将接收两个关键信息：`大章节名称` 和该章节下的 `小节列表`。
                * 你需要自行评估每个小节的知识点，识别出其中的"核心重点"、"难点"和"非重点（基础）"内容。

            2.  选择题（针对非重点和基础内容）：
                * 生成 3-5道 多项选择题。
                * 这些题目应侧重于章节中非核心、非难点但重要的基础知识，或概念的理解和记忆。
                * 每道选择题包含一个正确答案和至少3个合理干扰项。
                * 不提供答案。

            3.  问答题（针对核心重点和难点内容）：
                * 针对该章节的每个"核心重点"和"主要难点"，分别设计一道问答题。
                * 问答题应要求学生进行分析、解释、比较、应用或阐述等高阶思维活动。
                * 问题应清晰、明确，避免歧义，且能考察学生对该知识点的深入理解。
                * 不提供答案。

            4.  输出格式：

                ```
                ### 大章节名称 章节测试

                #### 一、选择题

                1. [选择题题目]
                A. [选项]
                B. [选项]
                C. [选项]
                D. [选项]
                2. ...

                #### 二、问答题

                1. [问答题题目]
                2. ...
                ```
            """),
            ("human", "{lessonPart}")
        ])
        
        # Initialize chains
        self.lesson_chain = LLMChain(
            llm=self.model,
            prompt=self.lesson_prompt,
            output_parser=self.lesson_parser
        )
        
        self.session_chain = LLMChain(
            llm=self.model,
            prompt=self.session_prompt,
            output_parser=self.session_parser
        )
        
        self.test_chain = LLMChain(
            llm=self.model,
            prompt=self.test_prompt,
            output_parser=self.test_parser
        )

    def genLesson(self, input: str):
        return self.lesson_chain.run(input=input)

    def genSession(self, session: str, lessonName: str):
        return self.session_chain.run(session=session, lessonName=lessonName)

    def genTest(self, lessonName: str, lessonPart: dict):
        return self.test_chain.run(lessonName=lessonName, lessonPart=str(lessonPart))

    def talkToModel(self, messages: list, jsonConvert: bool):
        resp = self.model.invoke(messages)
        if jsonConvert:
            return json.loads(resp.content.strip().removeprefix("```json\n").removesuffix("\n```"))
        return resp.content