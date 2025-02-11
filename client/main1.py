from fastapi import FastAPI, File, UploadFile, HTTPException
import tensorflow as tf
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = r"C:\Users\manvi\.vscode\python2-1\video.h5"
MODEL = tf.keras.models.load_model(MODEL_PATH)

CLASS_NAMES = {1: "one", 4: "four", 9: "nine"}  # Use a dictionary for class names

@app.post("/ping")
async def ping():
    return "Hello! Server is alive"

def read_file_as_image(data: bytes) -> np.ndarray:
    image = Image.open(BytesIO(data))

    # Convert image to RGB mode (if it has an alpha channel)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    resized_image = image.resize((200, 200), Image.LANCZOS)
    resized_np_image = np.array(resized_image)
    return resized_np_image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image = read_file_as_image(await file.read())
        img_batch = np.expand_dims(image, 0)
        predictions = MODEL.predict(img_batch)
        index = np.argmax(predictions[0])
        predicted_class = CLASS_NAMES.get(index, "Unknown")
        confidence = float(np.max(predictions[0]))

        return {
            'class': str(predicted_class),
            'confidence': confidence
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8091)
