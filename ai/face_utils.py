# ai/face_utils.py
import face_recognition
import numpy as np
import os

KNOWN_DIR = os.path.join(os.path.dirname(__file__), "known_faces")
THRESHOLD = 0.6

def load_known_faces():
    known_encodings = []
    names = []
    for file in os.listdir(KNOWN_DIR):
        path = os.path.join(KNOWN_DIR, file)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            names.append(file.split(".")[0])
    return known_encodings, names

def recognize_face(frame, known_encodings, names):
    rgb = frame[:, :, ::-1]  # Convert BGR to RGB
    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, faces)

    results = []
    for encoding, location in zip(encodings, faces):
        distances = face_recognition.face_distance(known_encodings, encoding)
        if len(distances) > 0 and min(distances) < THRESHOLD:
            match_index = np.argmin(distances)
            results.append((names[match_index], location))
        else:
            results.append(("Unknown", location))
    return results
