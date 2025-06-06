from model import LcModel
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mail import EmailSender  # 引用之前的 EmailSender 类

app = FastAPI()

@app.post("/send_lesson")
async def send_lesson(request: EmailRequest):
    """
    API to send a lesson email to the user.
    """

    raise HTTPException(status_code=500, detail="Failed to send email")
