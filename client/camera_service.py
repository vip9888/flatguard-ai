import cv2
import requests
import time

API_ENDPOINT = "http://127.0.0.1:8000/api/recognition/recognize/"

def capture_and_send():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        # Save frame temporarily
        image_path = "temp_frame.jpg"
        cv2.imwrite(image_path, frame)

        # Send image to Django API
        with open(image_path, 'rb') as img_file:
            files = {'image': img_file}
            try:
                response = requests.post(API_ENDPOINT, files=files)
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Match result: {result['match']}")
                    if result['match'] == "Unknown":
                        print("🚨 Alert: Unknown person detected!")
                else:
                    print(f"⚠️ Error: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"❌ API request failed: {e}")

        # Show frame
        cv2.imshow("FlatGuard Camera", frame)

        # Wait for 5 seconds before next capture
        if cv2.waitKey(5000) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_send()