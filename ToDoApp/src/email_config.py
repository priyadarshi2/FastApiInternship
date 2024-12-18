import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    #MAIL_TLS=os.getenv("MAIL_TLS").lower() in ["true", "1", "yes"], 
    #MAIL_SSL=os.getenv("MAIL_SSL").lower() in ["true", "1", "yes"], 
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS").lower() in ["true", "1", "yes"], 
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS").lower() in ["true", "1", "yes"], 
    MAIL_FROM=os.getenv("MAIL_FROM")
)
fm = FastMail(conf)
