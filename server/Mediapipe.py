from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
from math import dist

app = Flask(__name__)

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=4, static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.7)

# Initialize MediaPipe drawing module
mp_drawing = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                # Extract the coordinates of the desired landmarks (e.g., landmark 0 and landmark 9)
                coordinate_landmark_0 = (
                    int(landmarks.landmark[0].x * frame.shape[1]), int(landmarks.landmark[0].y * frame.shape[0]))
                coordinate_landmark_9 = (
                    int(landmarks.landmark[9].x * frame.shape[1]), int(landmarks.landmark[9].y * frame.shape[0]))

                # Draw landmarks and connections
                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS,
                                          landmark_drawing_spec=mp_drawing.DrawingSpec(
                                              color=(0, 255, 0), circle_radius=2),
                                          connection_drawing_spec=mp_drawing.DrawingSpec(
                                              color=(0, 0, 255), thickness=2))

                def x_coordinate(landmark):
                    return float(
                        str(results.multi_hand_landmarks[-1].landmark[int(landmark)]).split('\n')[0].split(" ")[1])

                def y_coordinate(landmark):
                    return float(
                        str(results.multi_hand_landmarks[-1].landmark[int(landmark)]).split('\n')[1].split(" ")[1])

                def finger(landmark, z):
                    if results.multi_hand_landmarks is not None:
                        try:
                            p0x = x_coordinate(0)
                            p0y = y_coordinate(0)
                            p3x = x_coordinate(3)
                            p3y = y_coordinate(3)
                            d03 = dist([p0x, p0y], [p3x, p3y])
                            p4x = x_coordinate(4)
                            p4y = y_coordinate(4)
                            d04 = dist([p0x, p0y], [p4x, p4y])
                            p7x = x_coordinate(7)
                            p7y = y_coordinate(7)
                            d07 = dist([p0x, p0y], [p7x, p7y])

                            p8x = x_coordinate(8)
                            p8y = y_coordinate(8)
                            d08 = dist([p0x, p0y], [p8x, p8y])
                            p11x = x_coordinate(11)
                            p11y = y_coordinate(11)
                            d011 = dist([p0x, p0y], [p11x, p11y])
                            p12x = x_coordinate(12)
                            p12y = y_coordinate(12)
                            d012 = dist([p0x, p0y], [p12x, p12y])
                            p15x = x_coordinate(15)
                            p15y = y_coordinate(15)
                            d015 = dist([p0x, p0y], [p15x, p15y])
                            p16x = x_coordinate(16)
                            p16y = y_coordinate(16)
                            d016 = dist([p0x, p0y], [p16x, p16y])
                            p19x = x_coordinate(19)
                            p19y = y_coordinate(19)
                            d019 = dist([p0x, p0y], [p19x, p19y])
                            p20x = x_coordinate(20)
                            p20y = y_coordinate(20)
                            d020 = dist([p0x, p0y], [p20x, p20y])

                            close = []

                            if z == "finger":
                                if d07 > d08:
                                    close.append(1)
                                if d011 > d012:
                                    close.append(2)
                                if d015 > d016:
                                    close.append(3)
                                if d019 > d020:
                                    close.append(4)
                                if d03 > d04:
                                    close.append(5)
                                return close
                            if z == "true coordinate":
                                plandmark_x = x_coordinate(landmark)
                                plandmark_y = x_coordinate(landmark)
                                return (int(1280 * plandmark_x), int(720 * plandmark_y))

                        except:
                            pass

                if finger(0, "finger") == [1, 2, 3, 4]:
                    if (orientation(finger(0, "true coordinate"), finger(9, "true coordinate")) == "Left") or (
                            orientation(finger(0, "true coordinate"), finger(9, "true coordinate")) == "Right"):
                        if finger(4, "true coordinate")[0] < finger(5, "true coordinate")[0]:
                            cv2.putText(frame, "Okay!!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

                def orientation(x, y):
                    x0 = x[0]
                    y0 = x[1]

                    x9 = y[0]
                    y9 = y[1]

                    if abs(x9 - x0) < 0.05:
                        m = 1000000000
                    else:
                        m = abs((y9 - y0) / (x9 - x0))

                    if m >= 0 and m <= 1:
                        if x9 < x0:
                            return 'Right'
                        else:
                            return 'Left'
                    if m > 1:
                        if y9 < y0:
                            return "up"
                        else:
                            return 'Down'

                points = []
                if finger(None, "finger") == [2, 3, 4, 5]:
                    points.append(finger(8, "true coordinate"))

                for i in range(len(points) - 1):
                    cv2.line(frame, (points[i][0], points[i][1]), (points[i + 1][0], points[i + 1][1]),
                             color=(255, 255, 0), thickness=1)

                direction = orientation(coordinate_landmark_0, coordinate_landmark_9)

                cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

                fingers_closed = finger(0, "finger")
                cv2.putText(frame, f"Fingers Closed: {fingers_closed}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (0, 255, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        data = []
        data.append(jpeg.tobytes())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + data[0] + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed_mp')
def video_feed_mp():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_python_file', methods=['POST'])
def stop_python_file():
    cap.release()
    return 'Python file stopped', 200
if __name__ == "__main__":
    app.run(port=8000,debug=True)