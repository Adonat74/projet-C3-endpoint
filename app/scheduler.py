import schedule
from datetime import date, datetime
from .database import get_db
from sqlalchemy.orm import Session
from .config import settings
from email.message import EmailMessage
import ssl
import smtplib
from fastapi import Depends
from . import models


def email(db: Session = Depends(get_db)):
    # if date.today().day != 14:
    #     return

    users = db.query(models.User).All()

    print(users)

    for x in users:
        email_sender = settings.email_sender
        email_password = settings.email_password
        subject = "Rappel saisie Chiffre d'affaire"
        body = f"Bonjour {x.first_name}, Noubliez pas de faire votre déclaration de chiffre d'affaire!"

        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = x.email
        em["Subject"] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, x.email, em.as_string())


schedule.every(10).seconds.do(email)

while True:
    schedule.run_pending()
