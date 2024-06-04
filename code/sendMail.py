import smtplib
from email.message import EmailMessage
import datetime
import os

maintenant=datetime.datetime.now()
dernier_envoi = datetime.datetime(2024, 5, 4)

# Fonction pour vérifier si un e-mail a déjà été envoyé pour un nom donné aujourd'hui
def est_deja_envoye(nom):
    aujourd_hui = datetime.datetime.now().date()
    fichier_log = "log_emails.txt"
    if os.path.exists(fichier_log):
        with open(fichier_log, "r") as f:
            lignes = f.readlines()
            for ligne in lignes:
                nom_enregistre, date_envoi = ligne.strip().split(",")
                date_envoi = datetime.datetime.strptime(date_envoi, "%Y-%m-%d").date()
                if nom == nom_enregistre and date_envoi == aujourd_hui:
                    return True
    return False


# Fonction pour enregistrer un e-mail envoyé dans le fichier de journal
def enregistrer_envoi(nom):
    aujourd_hui = datetime.datetime.now().date()
    fichier_log = "log_emails.txt"
    with open(fichier_log, "a") as f:
        f.write(f"{nom},{aujourd_hui}\n")


# Paramètres SMTP
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'bendebbayassmin@gmail.com'
smtp_password = 'gxcz jqfs wkfc tdup'
sender = 'bendebbayassmin@gmail.com'
recipient = 'eyayasmine6@gmail.com'
#fonction d'envoyer l'email
def send_email(subject, name):
    body = f"Mr/Mme {name} arrive en retard \n Il/Elle a pointé à {datetime.datetime.now().strftime('%H:%M:%S')} \n \n Cordialement"
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




