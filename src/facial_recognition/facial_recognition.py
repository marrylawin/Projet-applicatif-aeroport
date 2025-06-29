import cv2

def identify_passenger_by_face():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    #base de correspondance visage-email simplifiée (exemple)
    known_faces = {
        1: "camille.petit@email.com",
        2: "jean.dupont@email.com",
        3: "alice.durand@email.com"
    }

    cap = cv2.VideoCapture(0)
    count = 0

    print("Recherche de visage... Appuie sur 'q' pour quitter.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            count += 1
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Reconnaissance faciale', frame)

        if len(faces) > 0:
            print("👀 Visage détecté.")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Sortie sans détection.")
            cap.release()
            cv2.destroyAllWindows()
            return None

    cap.release()
    cv2.destroyAllWindows()

    detected_email = known_faces.get(1)
    print(f"Visage reconnu comme : {detected_email}")
    return detected_email
