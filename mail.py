import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient_email: str, subject: str, content: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(content, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable TLS
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

if __name__ == "__main__":
    sender = EmailSender(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        sender_email="your_email@gmail.com",
        sender_password="your_app_password"
    )
    
    success = sender.send_email(
        recipient_email="recipient@example.com",
        subject="Your Daily Lesson from HobbyLib",
        content="Welcome to your Python lesson! Today's topic: Variables and Data Types."
    )
