from flask import Flask, Response
import cv2


app = Flask(__name__)

face_cascade = cv2.CascadeClassifier(r"C:\Users\manvi\.vscode\python2-1\raw.githubusercontent.com_opencv_opencv_master_data_haarcascades_haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(r"C:\Users\manvi\.vscode\python2-1\raw.githubusercontent.com_opencv_opencv_master_data_haarcascades_haarcascade_eye.xml")
cap = cv2.VideoCapture(0)

def generate_frames():
    global cap  # Declare cap as a global variable

    while True:
        # Read a frame from the video stream
        ret, frm = cap.read()

        # Check if the frame is captured successfully
        if not ret:
            print("Error: Frame not captured successfully")
            continue  # Skip this iteration of the loop

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)

        # Handle empty frames
        if frm is None:
            print("Error: Empty frame")
            continue  # Skip this iteration of the loop

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Iterate over detected faces
        for (x, y, w, h) in faces:
            # Draw rectangles around faces
            cv2.rectangle(frm, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Extract the region of interest (ROI) for eye detection
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frm[y:y+h, x:x+w]

            # Detect eyes in the face region
            eyes = eye_cascade.detectMultiScale(roi_gray)

            # Iterate over detected eyes
            for (ex, ey, ew, eh) in eyes:
                # Draw rectangles around eyes
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        # Display the result
        # cv2.imshow('Face and Eye Detection in Video', frm)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret, jpeg = cv2.imencode('.jpg', frm)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    # Release the video capture object outside the loop
    cap.release()

@app.route('/video_feed_haar')
def video_feed_haar():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_python_file', methods=['POST'])
def stop_python_file():
    cap.release()

if __name__ == "__main__":
    # Use Gunicorn to run your Flask app
    # Specify the number of workers with the -w option
    # The syntax is: gunicorn -w <number_of_workers> -b <host:port> <your_app_script>:<your_flask_app_instance>
    # For example, running on localhost at port 5000 with 4 workers:
    # gunicorn -w 4 -b 127.0.0.1:5000 app:app
 app.run(port=8080,debug=True)