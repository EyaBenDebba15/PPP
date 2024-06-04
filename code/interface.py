import streamlit as st
import pandas as pd
import mysql.connector
import base64
from streamlit.components.v1 import html
import datetime

#Page set up
st.set_page_config(page_title="Entreprise", 
                   page_icon=":office:",
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )

#Sidebar
######

st.sidebar.title(":raised_hand_with_fingers_splayed: je veux")
nav = st.sidebar.radio('',['PAGE D\'ACCEUIL', 'PRESENTATION DES EMPLOYÉS', 'LISTE DES POINTAGES', 'VISUALISER PAR PERSONNES','VISUALISER PAR DATE'])

#######
#PAGES
######

#Page d'acceuil
#####

if nav == 'PAGE D\'ACCEUIL':
    st.title('Saluut')

# Connexion à la base de données
connection = mysql.connector.connect(host="localhost", user="root", password="", database="entreprise")
cursor = connection.cursor()

#Presentation des personnels
#####

if nav == 'PRESENTATION DES EMPLOYÉS':
    st.title(":male-office-worker: Personnel")


    # Fonction pour convertir les données binaires d'une image en base64
    def image_to_base64(image_data):
        return base64.b64encode(image_data).decode()

    # Fonction pour formater une image en balise HTML
    def image_formatter(image_data):
        image_base64 = image_to_base64(image_data)
        return f'<img src="data:image/png;base64,{image_base64}" width="100" />'

    @st.cache_data
    def convert_df(input_df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        df = input_df.copy()
        df['image'] = df['image'].apply(image_formatter)
        return df.to_html(escape=False, index=False)

    # Vérifier si la connexion est établie
    if connection.is_connected():
        print("Connexion à la base de données réussie.")
    else:
        print("Échec de la connexion à la base de données.")

    # Requête pour récupérer les données de la table (y compris les images)
    query = "SELECT id, nom, prenom, image FROM personnel"
    df = pd.read_sql(query, connection)

    # Afficher le tableau avec les images
    st.markdown(convert_df(df), unsafe_allow_html=True)

    # Fermer la connexion à la base de données
    connection.close()




#Pointage par date
#####
if nav == 'LISTE DES POINTAGES':
    st.title(":clock8: POINTAGE")
    st.write('Le tableau de pointage enregistre les entrées des employés.\n\n Il contient les informations suivantes pour chaque enregistrement :\n\n ID : Identifiant unique de l\'employé.\n\n Date : La date à laquelle l\'employé a enregistré son pointage.\n\n Heure : L\'heure à laquelle l\'employé a enregistré son pointage.')
    query_pointage = "SELECT id, date, heure From pointage"
    df_pointage = pd.read_sql(query_pointage, connection)
    df_pointage['heure'] = df_pointage['heure'].apply(lambda x: (datetime.datetime.min + x).time().strftime('%H:%M:%S'))
    st.table(df_pointage)



#Selection
#####
if nav == 'VISUALISER PAR PERSONNES':
    # Sélectionner l'employé
    cursor.execute("SELECT nom,prenom FROM personnel")
    results = cursor.fetchall()
    employe_selec = st.sidebar.selectbox("Sélectionnez l'employé", results)
    nom_selec, prenom_selec = employe_selec

    cursor.execute("SELECT id, date, heure From pointage  WHERE id= (SELECT id FROM personnel WHERE nom = %s AND prenom = %s)",(nom_selec, prenom_selec))
    select_pers = cursor.fetchall()
    df_pers = pd.DataFrame(select_pers, columns=['id', 'date', 'heure'])
    # Formater la colonne 'heure' au format heure
    df_pers['heure'] = df_pers['heure'].apply(lambda x: (datetime.datetime.min + x).time().strftime('%H:%M:%S'))
    st.table(df_pers)


if nav == 'VISUALISER PAR DATE':
    # Sélectionner une date
    selected_date = st.sidebar.date_input("Sélectionnez une date")

    # Convertir la date sélectionnée en format SQL
    selected_date_sql = selected_date.strftime('%Y-%m-%d')

    # Exécuter la requête SQL pour récupérer les données de pointage pour la date sélectionnée
    cursor.execute("""
        SELECT p.id, p.date, p.heure, pe.nom, pe.prenom 
        FROM pointage p 
        INNER JOIN personnel pe ON p.id = pe.id 
        WHERE p.date = %s
        """, (selected_date_sql,))
    select_date = cursor.fetchall()

    # Créer un DataFrame pandas à partir des résultats
    df_date = pd.DataFrame(select_date, columns=['id', 'date', 'heure', 'nom', 'prenom'])

    # Formater la colonne 'heure' au format heure
    df_date['heure'] = df_date['heure'].apply(lambda x: (datetime.datetime.min + x).time().strftime('%H:%M:%S'))

    # Afficher le DataFrame dans une table
    st.table(df_date)


