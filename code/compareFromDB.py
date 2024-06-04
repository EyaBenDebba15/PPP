import mysql.connector
from PIL import Image
import io
import cv2
import numpy as np
import face_recognition
import datetime
from datetime import time
import sendMail
import arduino

# Connect to the database
connection = mysql.connector.connect(host="localhost", user="root", password="", database="entreprise")

if connection.is_connected():
    print("Connected successfully")
else:
    print('Failed to connect')

cursor = connection.cursor()

# Retrieve images from the database
cursor.execute("SELECT image FROM personnel")
results = cursor.fetchall()

# Load known face encodings and names
known_face_encodings = []
known_face_names = []

for result in results:
    # Convert blob data to numpy array
    image_data = result[0]
    image = Image.open(io.BytesIO(image_data))
    # Convert PIL image to numpy array
    image_np = np.array(image)
    # Convert image from RGB (PIL) to BGR (OpenCV)
    rgb_img = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    # Find face encodings
    face_encodings = face_recognition.face_encodings(rgb_img)
    if len(face_encodings) > 0:
        known_face_encodings.append(face_encodings[0])
        cursor.execute("SELECT nom, prenom FROM personnel WHERE image = %s", (image_data,))
        name_result = cursor.fetchone()
        if name_result:
            nom, prenom = name_result
            full_name = f"{prenom} {nom}"
            known_face_names.append(full_name)
        else:
            known_face_names.append("Unknown")

# Load camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Detect faces
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    face_names = []
    command_sent = False 
    for face_encoding in face_encodings:
        # Compare faces with known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            prenom, nom = name.split(' ')
            cursor.execute("SELECT EXISTS (SELECT 1 FROM pointage WHERE id= (SELECT id FROM personnel WHERE nom = %s AND prenom = %s) AND date = %s) AS personnel_present",(nom,prenom,datetime.datetime.now().date()))
            x=cursor.fetchone()
            if x[0] == 0:
                cursor.execute("INSERT INTO pointage (id, date, heure) SELECT (select p.id FROM personnel p WHERE p.nom = %s AND p.prenom = %s ),%s,%s",((nom, prenom,datetime.datetime.now().date(),datetime.datetime.now().time())))
            #send MAIL
            if not sendMail.est_deja_envoye(name) and datetime.datetime.now().time() > time(8,30):
                sendMail.send_email('Reclamation de retard', name)
                sendMail.enregistrer_envoi(name)
            #ouvrir port
            if not command_sent:
                response = arduino.send_command('on')
                command_sent = True
            connection.commit()

        face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow('Face Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()

# Close connection to the database
cursor.close()
connection.close()

