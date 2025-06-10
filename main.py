from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
from typing import List
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from model import Ai_model
from mail import EmailSender
from pg import Pg 

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀...")
    db = Pg("localhost", "hobby-lib", "myuser", "password", "5432")
    await db.create_pool()

    email_sender = EmailSender(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        sender_email="yanshuai9604@gmail.com",
        sender_password=os.environ['gmail_pwd']
    )
    ai_model = Ai_model()

    app.state.db = db
    app.state.email_sender = email_sender
    app.state.ai_model = ai_model

    scheduler = AsyncIOScheduler()

    scheduler.add_job(send_lesson, CronTrigger(minute=0), args=[app])
    scheduler.start()

    yield

    print("Close...")
    await app.state.db.close_pool()
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)


class EmailRequest(BaseModel):
    email: str
    lessonName: str
    lessonTime: List[int]

async def send_lesson(app_instance: FastAPI):
    print(f"[{datetime.datetime.now()}] 开始执行 send_lesson 任务...")
    current_hour = datetime.datetime.now().hour
    
    db = app_instance.state.db
    ai_model = app_instance.state.ai_model
    email_sender = app_instance.state.email_sender

    need_send_sessions = await db.get_need_send_lesson(current_hour)
    need_send_tests = await db.get_need_send_test(current_hour)

    for session in need_send_sessions:
        sessionContent = ai_model.genSession()
        email_sender.send_email(session.email, sessionContent.title, sessionContent)
        print(f"已为 {session.email} 发送课程提醒。")

    for test in need_send_tests:
        testContent = ai_model.genTest()
        email_sender.send_email(test.email, testContent.title, testContent)
        print(f"已为 {test.email} 发送测试提醒。")


@app.post("/registe_lesson")
async def registe_lesson(req: Request, lesson_request: EmailRequest):
    db = req.app.state.db
    ai_model = req.app.state.ai_model
    
    email = lesson_request.email
    lessonName = lesson_request.lessonName

    lesson = ai_model.genLesson(lessonName)

    if hasattr(lesson, 'invalid') and lesson.invalid:
        raise HTTPException(status_code=501, detail="Invalid lesson name")
    
    await db.create_lesson({
        "email": email,
        "lessonName": lessonName,
        "lessonContent": lesson,
        "process": [0, 0],
        "finish": False,
        "lessonTime": lesson_request.lessonTime
    })

    return lesson

