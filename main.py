from model import Ai_model
from fastapi import FastAPI, HTTPException
from mail import EmailSender
from pydantic import BaseModel
from typing import List
import schedule
import time
import datetime
from pg import Pg

app = FastAPI()

db = Pg({
    "host": "localhost",
    "database": "hobby-lib",
    "user": "myuser",
    "password": "password",
    "port": "5432"
})
db.create_connection()
email_sender = EmailSender()

class EmailRequest(BaseModel):
    email: str
    lessonName: str
    lessonTime: List[int]

ai_model = Ai_model()

def send_lesson():
    current_hour = datetime.datetime.now().strftime("%H")
    need_send_sessions = db.get_need_send_lesson(current_hour)
    need_send_tests = db.get_need_send_test(current_hour)

    for session in need_send_sessions:
        sessionContent = ai_model.genSession()
        email_sender.send_email(sessionContent.title)

    for test in need_send_tests:
        testContent = ai_model.genTest()
        email_sender.send_email(testContent)  


schedule.every().hour.at(":00").do(send_lesson)


@app.post("/registe_lesson")
async def registe_lesson(request: EmailRequest):
    # getparam -> pass to model -> get model response -> insert to db -> return lesson
    email = request.email
    lessonName = request.lessonName

    lesson = ai_model.genLesson(lessonName)

    if lesson.invalid:
        raise HTTPException(status_code=501, detail=f"invalid lesson name")
    
    db.create_lesson({
        email: email,
        lessonName: lessonName,
        "lessonContent":lesson,
        process: [0,0],
        finish: false,
        lessonTime: 18 # type: ignore
    })

    return lesson