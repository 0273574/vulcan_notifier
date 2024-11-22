import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

class EmailSender:
    def __init__(self, email_config):
        self.config = email_config

    async def send_notification(self, subject: str, message: str):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.sender_email
            msg['To'] = self.config.recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.sender_email, self.config.sender_password)
                server.send_message(msg)
            
            logging.info(f"Wysłano powiadomienie: {subject}")
        except Exception as e:
            logging.error(f"Błąd wysyłania e-maila: {e}")
