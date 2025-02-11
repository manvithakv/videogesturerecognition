
from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8888"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = load_model(r"C:\Users\manvi\.vscode\python2-1\video.h5")

MAX_FRAMES = 150  # Maximum number of frames to process

# Dictionary to map predicted class indices to labels
class_labels = {
    1: "one",
    4: "four",
    9: "nine",
}

def process_video(file_path: str) -> dict:
    cap = cv2.VideoCapture(file_path)

    # Dictionary to store the count of each predicted class
    class_counts = {}

    frame_counter = 0  # Counter to track the number of processed frames

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret or frame_counter >= MAX_FRAMES:
            break

        # Resize the frame to match the model's expected input shape (50x50)
        processed_frame = cv2.resize(frame, (200, 200))
        processed_frame = processed_frame.astype(float)

        # Make a prediction using the loaded model
        prediction = MODEL.predict(np.expand_dims(processed_frame, axis=0))[0]
        predicted_class = np.argmax(prediction)

        # Update the count for the predicted class in the dictionary
        class_counts[predicted_class] = class_counts.get(predicted_class, 0) + 1

        frame_counter += 1

    # Release video capture
    cap.release()

    # Find the class with the maximum count
    max_class = int(max(class_counts, key=class_counts.get))  # Convert to integer

    # Map the predicted class to the corresponding label
    predicted_label = class_labels.get(max_class, "Unknown")

    return {"max_predicted_class": max_class, "predicted_label": predicted_label, "class_counts": class_counts}

@app.post("/predict_video")
async def predict_video(file: UploadFile = File(...)):
    try:
        video_bytes = await file.read()
        video_path = "input_video.mp4"
        with open(video_path, "wb") as video_file:
            video_file.write(video_bytes)

        print("Video saved successfully")

        result = process_video(video_path)

        print("Video processed successfully")

        return {"max_predicted_class": result["max_predicted_class"], "predicted_label": result["predicted_label"]}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8060)