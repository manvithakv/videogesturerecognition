from flask import Flask, render_template, Response
import cv2
import numpy as np

background = None
frames_elapsed = 0
FRAME_HEIGHT = 450
FRAME_WIDTH = 600
CALIBRATION_TIME = 30
OBJ_THRESHOLD = 18

top = (0, 0)
bottom = (0, 0)
left = (0, 0)
right = (0, 0)
centerX = 0

isInFrame = False
isWaving = False
fingers = None
gestureList = []

app = Flask(__name__)

def update_hand_data(l, t, r, b, cx):
    global top, bottom, left, right, centerX
    top, bottom, left, right, centerX = t, b, l, r, cx

def check_for_waving(cx):
    global isWaving, centerX
    prevCenterX = centerX
    centerX = cx
    if abs(centerX - prevCenterX) > 3:
        isWaving = True
    else:
        isWaving = False

def most_frequent(input_list):
    freq_dict = {}
    count = 0
    most_freq = 0
    for item in reversed(input_list):
        freq_dict[item] = freq_dict.get(item, 0) + 1
        if freq_dict[item] >= count:
            count, most_freq = freq_dict[item], item
    return most_freq

def count_fingers(thresholded_image):
    global top, bottom, left, right
    line_height = int(top[1] + (0.2 * (bottom[1] - top[1])))
    line = np.zeros(thresholded_image.shape[:2], dtype=int)
    cv2.line(line, (thresholded_image.shape[1], line_height), (0, line_height), 255, 1)
    line = cv2.bitwise_and(thresholded_image, thresholded_image, mask=line.astype(np.uint8))
    contours, _ = cv2.findContours(line.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    fingers_count = 0
    for curr in contours:
        width = len(curr)
        if width < 3 * abs(right[0] - left[0]) / 4 and width > 5:
            fingers_count += 1
    return fingers_count

def write_on_image(frame):
    global isInFrame, isWaving, fingers
    text = "Searching..."
    if frames_elapsed < CALIBRATION_TIME:
        text = "Calibrating..."
    elif not isInFrame:
        text = "No hand detected"
    else:
        if isWaving:
            text = "Waving"
        elif fingers == 0:
            text = "Rock"
        elif fingers == 1:
            text = "Pointing"
        elif fingers == 2:
            text = "Scissors"
    cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.rectangle(frame, (region_left, region_top), (region_right, region_bottom), (255, 255, 255), 2)

region_top = 0
region_bottom = int(FRAME_HEIGHT / 2)
region_left = int(FRAME_WIDTH / 2)
region_right = FRAME_WIDTH

capture = cv2.VideoCapture(0)

def get_frame():
    global capture, background, frames_elapsed, isInFrame, isWaving, fingers, gestureList
    while True:
        success, frame = capture.read()
        if not success:
            break
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        frame = cv2.flip(frame, 1)

        region = frame[region_top:region_bottom, region_left:region_right]
        region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        region = cv2.GaussianBlur(region, (5, 5), 0)

        if frames_elapsed < CALIBRATION_TIME:
            if background is None:
                background = region.copy().astype("float")
        else:
            diff = cv2.absdiff(background.astype(np.uint8), region)
            thresholded_region = cv2.threshold(diff, OBJ_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
            contours, _ = cv2.findContours(thresholded_region.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) == 0:
                isInFrame = False
            else:
                isInFrame = True
                segmented_region = max(contours, key=cv2.contourArea)
                update_hand_data(*tuple(segmented_region[segmented_region[:, :, i].argmin()][0] for i in range(2)),
                                 *tuple(segmented_region[segmented_region[:, :, i].argmax()][0] for i in range(2)),int((left[0] + right[0]) / 2))
                if frames_elapsed % 6 == 0:
                    check_for_waving(int((left[0] + right[0]) / 2))
                gestureList.append(count_fingers(thresholded_region))
                if frames_elapsed % 12 == 0:
                    fingers = most_frequent(gestureList)
                    gestureList.clear()

        write_on_image(frame)
        _, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        frames_elapsed += 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_python_file', methods=['POST'])
def stop_python_file():
    capture .release()
if __name__ == '__main__':
    app.run(debug=True)