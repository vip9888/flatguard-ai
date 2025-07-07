import cv2
import os
from deepface_utils import verify_face_with_known, find_best_match

print("[INFO] Starting webcam...")
cap = cv2.VideoCapture(0)

# Configuration
THRESHOLD = 0.6  # Adjust this value (lower = more strict)
MODEL_NAME = "VGG-Face"  # Try different models: VGG-Face, Facenet, OpenFace, DeepID
SKIP_FRAMES = 5  # Process every Nth frame to improve performance

frame_count = 0
last_result = "Unknown"
last_distance = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Failed to grab frame.")
        break

    frame_count += 1
    
    # Only process every Nth frame to improve performance
    if frame_count % SKIP_FRAMES != 0:
        # Draw the last result
        cv2.putText(frame, last_result, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 
                    (0, 255, 0) if "Unknown" not in last_result else (0, 0, 255), 2)
        cv2.imshow("DeepFace Camera", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # Save current frame temporarily to compare
    temp_path = "temp_frame.jpg"
    cv2.imwrite(temp_path, frame)

    try:
        # Compare with known faces
        print(f"\n--- Frame {frame_count} ---")
        matches = verify_face_with_known(temp_path, model_name=MODEL_NAME, threshold=THRESHOLD)
        
        # Find the best match
        best_name, best_distance = find_best_match(matches)
        
        if best_name:
            last_result = f"{best_name} ({best_distance:.3f})"
            last_distance = best_distance
            print(f"✓ MATCH: {last_result}")
        else:
            last_result = "Unknown"
            print(f"✗ NO MATCH - Best distance: {min([m[1] for m in matches]) if matches else 'N/A'}")
            
    except Exception as e:
        print(f"Error in face verification: {e}")
        last_result = "Error"

    # Draw label
    color = (0, 255, 0) if "Unknown" not in last_result else (0, 0, 255)
    cv2.putText(frame, last_result, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    # Draw configuration info
    cv2.putText(frame, f"Model: {MODEL_NAME}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, f"Threshold: {THRESHOLD}", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("DeepFace Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if os.path.exists("temp_frame.jpg"):
    os.remove("temp_frame.jpg")
