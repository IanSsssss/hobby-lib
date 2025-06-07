from model import LcModel
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mail import EmailSender  # 引用之前的 EmailSender 类

app = FastAPI()

class EmailRequest(BaseModel):
    email: str
    lesson: str

@app.post("/send_lesson")
async def registe_lesson(request: EmailRequest):
    try:
        email = request.email
        lesson = request.lesson

        if email == "ys0430ys@sina.com":
            return {"message": "Email sent successfully", "email": email, "lesson": lesson}
        else:
            raise HTTPException(status_code=400, detail="Invalid email address")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
