import mysql.connector
from PIL import Image
import io

connection= mysql.connector.connect(host="localhost",user="root",password="",database="entreprise")

if connection.is_connected():
    print("connected successfully")
else:
    print('failed')

curseur=connection.cursor()
curseur.execute("SELECT image FROM personnel")
resultats=curseur.fetchall()

curseur.close()
connection.close()

for resultat in resultats :
    donnees_image = resultat[0]  # Supposons que la colonne image est la première dans le résultat
    image = Image.open(io.BytesIO(donnees_image))
    image.show()