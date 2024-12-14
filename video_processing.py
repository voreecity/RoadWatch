import cv2
import os
import math
import time
import numpy as np
import cvzone
from ultralytics import YOLO
from sort import Sort


def process_video(video_file_location, speed_checkbox_value, classname_checkbox_value, outgoing_checkbox_value,
                  oncoming_checkbox_value):
    cap = cv2.VideoCapture(video_file_location)
    model = YOLO("../Yolo-weights/yolov8s.pt")

    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                  "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog",
                  "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                  "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
                  "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass",
                  "cup",
                  "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot",
                  "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed", "diningtable",
                  "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven",
                  "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
                  "toothbrush"]

    current_directory = os.path.dirname(os.path.abspath(__file__))
    mask_path = os.path.join(current_directory, "mask.png")
    mask = cv2.imread(mask_path)

    # Tracking
    tracker = Sort(20, 3, 0.3)

    # Line
    limitsUp = [250, 800, 920, 800]
    limitsDown = [975, 800, 1700, 800]

    totalCountUp = []
    totalCountDown = []

    carPositions = {}

    while True:
        success, img = cap.read()
        imgRegion = cv2.bitwise_and(img, mask)
        graphics_path = os.path.join(current_directory, "graphics.png")
        imgGraphics = cv2.imread(graphics_path, cv2.IMREAD_UNCHANGED)
        img = cvzone.overlayPNG(img, imgGraphics, (0, 0))

        results = model(imgRegion, stream=True)

        detections = np.empty((0, 5))

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                w, h = x2 - x1, y2 - y1

                # Confidence Value
                conf = math.ceil((box.conf[0] * 100)) / 100

                # Class Names
                cls = int(box.cls[0])
                currentClass = classNames[cls]

                if currentClass == "car" or currentClass == "bus" or currentClass == "truck" and conf > 0.3:
                    currentArray = np.array([x1, y1, x2, y2, conf])
                    detections = np.vstack((detections, currentArray))

        resultsTracker = tracker.update(detections)
        cv2.line(img, (limitsUp[0], limitsUp[1]), (limitsUp[2], limitsUp[3]), (0, 0, 255), 5)
        cv2.line(img, (limitsDown[0], limitsDown[1]), (limitsDown[2], limitsDown[3]), (0, 0, 255), 5)

        for result in resultsTracker:
            x1, y1, x2, y2, id = result
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            print(result)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h), 15, 2, colorR=(255, 0, 0))
            cx, cy = x1 + w // 2, y1 + h // 2
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

            if limitsUp[0] < cx < limitsUp[2] and limitsUp[1] - 15 < cy < limitsUp[3] + 15:
                if totalCountUp.count(id) == 0:
                    totalCountUp.append(id)
                    cv2.line(img, (limitsUp[0], limitsUp[1]), (limitsUp[2], limitsUp[3]), (0, 255, 0), 5)
            if limitsDown[0] < cx < limitsDown[2] and limitsDown[1] - 15 < cy < limitsDown[3] + 15:
                if totalCountDown.count(id) == 0:
                    totalCountDown.append(id)
                    cv2.line(img, (limitsDown[0], limitsDown[1]), (limitsDown[2], limitsDown[3]), (0, 255, 0), 5)

            if id not in carPositions:
                carPositions[id] = {'position': (cx, cy), 'timestamp': time.time()}
            else:
                # Calculate the distance traveled by the car in pixels
                distance_pixels = math.sqrt(
                    (cx - carPositions[id]['position'][0]) ** 2 + (cy - carPositions[id]['position'][1]) ** 2)

                # Convert the distance from pixels to meters
                distance_meters = distance_pixels / 150

                # Calculate the time taken in seconds
                time_taken = time.time() - carPositions[id]['timestamp']

                # Take into account the speed of the video
                time_taken = time_taken / 5

                # Calculate the speed of the car in meters per second
                speed_mps = distance_meters / time_taken

                # Convert the speed from meters per second to kilometers per hour
                speed_kmph = math.ceil(speed_mps * 3.6)

                # Display the speed of the car
                if speed_checkbox_value:
                    cvzone.putTextRect(img, f'{speed_kmph} km/h', (max(0, x1), max(35, y1)), 2, 2,
                                       (255, 255, 255), (73, 24, 214))

                if classname_checkbox_value:
                    cvzone.putTextRect(img, f'{classNames[cls]}', (max(0, x1), max(35, y1)), 2, 2,
                                       (255, 255, 255), (73, 24, 214))

                if speed_checkbox_value and classname_checkbox_value:
                    cvzone.putTextRect(img, f'{classNames[cls]}: {speed_kmph} km/h', (max(0, x1), max(35, y1)), 2, 2,
                                       (255, 255, 255), (73, 24, 214))

        if outgoing_checkbox_value:
            cv2.putText(img, f'Oncoming:', (200, 20), cv2.FONT_ITALIC, 1, (255, 0, 0), 3)
            cv2.putText(img, f'{len(totalCountUp)}', (200, 50), cv2.FONT_ITALIC, 1, (0, 0, 255), 3)

        if oncoming_checkbox_value:
            cv2.putText(img, f'Outgoing:', (200, 90), cv2.FONT_ITALIC, 1, (255, 0, 0), 3)
            cv2.putText(img, f'{len(totalCountDown)}', (200, 120), cv2.FONT_ITALIC, 1, (0, 0, 255), 3)

        cv2.imshow("Video", img)
        cv2.waitKey(1)