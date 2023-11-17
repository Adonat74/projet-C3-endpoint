import schedule
from datetime import date, datetime
from database import get_db, SessionLocal
from sqlalchemy import text
from config import settings
from email.message import EmailMessage
import ssl
import smtplib
from fastapi import Depends
import models


# def email(db=SessionLocal):
#     # db: Session = Depends(get_db)
#     # if date.today().day != 5:
#     #     return

#     users = db().query(models.User).all()

#     print(users)

#     for x in users:
#         email_sender = settings.email_sender
#         email_password = settings.email_password
#         subject = "Rappel saisie Chiffre d'affaire"
#         body = f"Bonjour {x.first_name}, Noubliez pas de faire votre déclaration de chiffre d'affaire!"

#         em = EmailMessage()
#         em["From"] = email_sender
#         em["To"] = x.email
#         em["Subject"] = subject
#         em.set_content(body)

#         context = ssl.create_default_context()

#         with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
#             smtp.login(email_sender, email_password)
#             smtp.sendmail(email_sender, x.email, em.as_string())


def new_email(db=SessionLocal):
    db: Session = Depends(get_db)
    if date.today().day != 5:
        return

    req = text("""SELECT * FROM delay_user""")

    users = db().execute(req).all()

    print(users)

    for x in users:
        print(x)
        email_sender = settings.email_sender
        email_password = settings.email_password
        subject = "Rappel saisie Chiffre d'affaire"
        body = f"Bonjour {x[1]}, Noubliez pas de faire votre déclaration de chiffre d'affaire!"

        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = x[0]
        em["Subject"] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, x[0], em.as_string())


if __name__ == "__main__":
    new_email()
    schedule.every().day.do(new_email(db))

    while True:
        schedule.run_pending()
