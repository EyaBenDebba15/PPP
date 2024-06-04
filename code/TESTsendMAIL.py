import smtplib
from email.message import EmailMessage
import datetime
import os

# Paramètres SMTP
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'bendebbayassmin@gmail.com'
smtp_password = 'gxcz jqfs wkfc tdup'
sender = 'bendebbayassmin@gmail.com'
recipient = 'eyayasmine6@gmail.com'


#fonction d'envoyer l'email
def send_email(subject, name,signature):
    body = f"Dear {name} \n I hope you are doing well \n {signature}"
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        print('E-mail envoyé avec succès !')
    except Exception as e:
        print(f'Erreur lors de l\'envoi de l\'e-mail : {str(e)}')
    finally:
        server.quit()
