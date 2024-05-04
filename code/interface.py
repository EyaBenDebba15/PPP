import streamlit as st
import pandas as pd
import mysql.connector
import base64
from streamlit.components.v1 import html

#Page set up
st.set_page_config(page_title="Entreprise", 
                   page_icon=":office:",
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )

st.sidebar.title(":raised_hand_with_fingers_splayed: je veux")
nav = st.sidebar.radio('',['Page d\'acceuil', 'Presentation des personnels', 'Pointage par date', 'Analyser par personne'])

#######
#PAGES
######

#Page d'acceuil
#####

if nav == 'Page d\'acceuil':
    st.title('Saluut')




#Presentation des personnels
#####

if nav == 'Presentation des personnels':
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


    # Connexion à la base de données
    connection = mysql.connector.connect(host="localhost", user="root", password="", database="entreprise")

    # Vérifier si la connexion est établie
    if connection.is_connected():
        print("Connexion à la base de données réussie.")
    else:
        print("Échec de la connexion à la base de données.")

    # Requête pour récupérer les données de la table (y compris les images)
    query = "SELECT id, nom, prenom, image, temps FROM personnel"
    df = pd.read_sql(query, connection)

    # Afficher le tableau avec les images
    st.markdown(convert_df(df), unsafe_allow_html=True)

    # Fermer la connexion à la base de données
    connection.close()




#Pointage par date
#####
