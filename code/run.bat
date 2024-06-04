@echo off

rem Executer interface 
start "" streamlit run c:\Users\Utilisateur\Desktop\PPP\faceRECOGNITION\code\interface.py --server.headless true --server.port 8501

rem Attendre quelques secondes pour permettre à l'interface de démarrer
rem timeout /t 5

rem Executer compareFromDB
rem start "" python compareFromDB.py

rem Executer sendMail
rem start "" python sendMail.py