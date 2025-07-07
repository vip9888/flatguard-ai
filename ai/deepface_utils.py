from deepface import DeepFace
import os
import cv2
import numpy as np

# Directory to store known face images
KNOWN_DIR = os.path.join(os.path.dirname(__file__), "known_faces")

def verify_face_with_known(frame, model_name="VGG-Face", threshold=0.6):
    """
    Verify face with known faces using DeepFace
    
    Args:
        frame: Path to the current frame image
        model_name: DeepFace model to use (VGG-Face, Facenet, OpenFace, etc.)
        threshold: Similarity threshold (lower = more strict)
    
    Returns:
        List of tuples: (name, distance, verified)
    """
    results = []
    
    if not os.path.exists(KNOWN_DIR):
        print(f"Warning: Known faces directory {KNOWN_DIR} does not exist")
        return results
    
    for filename in os.listdir(KNOWN_DIR):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            continue
            
        known_path = os.path.join(KNOWN_DIR, filename)
        name = os.path.splitext(filename)[0]

        try:
            print(f"Comparing with {name}...")
            
            # Compare webcam frame with each known image
            result = DeepFace.verify(
                img1_path=frame,
                img2_path=known_path,
                model_name=model_name,
                detector_backend="mtcnn",
                enforce_detection=False,
                distance_metric="cosine"  # Use cosine distance for better results
            )

            distance = result["distance"]
            verified = result["verified"]
            
            print(f"  Distance: {distance:.4f}, Verified: {verified}")
            
            # Use custom threshold instead of DeepFace's default
            if distance < threshold:
                results.append((name, distance, True))
            else:
                results.append((name, distance, False))
                
        except Exception as e:
            print(f"Error comparing to {filename}: {e}")
            results.append((name, float('inf'), False))

    return results

def find_best_match(results):
    """
    Find the best match from verification results
    
    Args:
        results: List of tuples (name, distance, verified)
    
    Returns:
        Tuple: (name, distance) or (None, None) if no good match
    """
    if not results:
        return None, None
    
    # Sort by distance (lower is better)
    results.sort(key=lambda x: x[1])
    
    # Get the best match
    best_name, best_distance, best_verified = results[0]
    
    # If the best match is verified, return it
    if best_verified:
        return best_name, best_distance
    
    return None, None
