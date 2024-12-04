from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText
import smtplib


# SMTP configuration for MailHog
SMTP_SERVER = 'localhost'
SMTP_PORT = 1025
SENDER_EMAIL = ''
SENDER_PASSWORD = ''


def send_email(From, to, subject, content_body):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg["To"] = to
        msg["Subject"] = subject
        msg["From"] = From
        msg.attach(MIMEText(content_body, 'html'))

        # Connect to SMTP server and send the email
        with smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT) as client:
            client.send_message(msg=msg)
        print(f"Email sent successfully to {to}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False