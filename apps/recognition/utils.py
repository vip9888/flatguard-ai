import os
from ai.deepface_utils import verify_face_with_known


def verify_face_and_return_match(image_path):
    try:
        matches=verify_face_with_known(image_path)
        if matches:
            matches.sort(key=lambda x: x[1]) #sort by distance
            return matches
        return []

    except Exception as e:
        print(f"Error in face verification: {e}")
        return []