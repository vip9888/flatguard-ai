import os
from ai.deepface_utils import verify_face_with_known, find_best_match


def verify_face_and_return_match(image_path):
    try:
        matches = verify_face_with_known(image_path)
        if matches:
            # Find the best match
            best_name, best_distance = find_best_match(matches)
            if best_name:
                return [(best_name, best_distance)]
        return []

    except Exception as e:
        print(f"Error in face verification: {e}")
        return []