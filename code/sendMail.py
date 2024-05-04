import smtplib
from email.message import EmailMessage
import compareFromDB

# Paramètres SMTP
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'bendebbayassmin@gmail.com'
smtp_password = 'gxcz jqfs wkfc tdup'
sender = 'bendebbayassmin@gmail.com'
recipient = 'eyayasmine6@gmail.com'




def send_email(subject, body, attachment_path=None):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        body="Mr/Mme %s fait un retard \n Cordialement",(compareFromDB.name)
        server.send_message(msg)
        print('E-mail envoyé avec succès !')
    except Exception as e:
        print(f'Erreur lors de l\'envoi de l\'e-mail : {str(e)}')
    finally:
        server.quit()

if len(compareFromDB.face_encodings) > 0:
    send_email('Reclamation de retard',send_email.body,)


    