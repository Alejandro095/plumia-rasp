from ultralytics import YOLO
import cv2
import numpy as np
from time import time

from alpr.utils import read_license_plate

def read_number_plate(callback, input):
    try:
        # load models
        license_plate_detector = YOLO('./src/alpr/models/license_plate_detector.pt')

        # load video
        cap = cv2.VideoCapture(0)

        # read frames
        prev = 0
        ret = True
        while ret:
            ret, frame = cap.read()

            time_elapsed = time() - prev
            if time_elapsed > 5:
                prev = time()

                if (not input.is_active):
                    return

                if ret:
                    # detect license plates
                    license_plates = license_plate_detector(frame)[0]
                    for license_plate in license_plates.boxes.data.tolist():
                        x1, y1, x2, y2, score, class_id = license_plate

                        # crop license plate
                        license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                        # process license plate
                        gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)

                        threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

                        # read license plate number
                        license_plate_text = read_license_plate(threshold)

                        if (license_plate_text is not None):
                            result = callback(license_plate_text)

                            if (result):
                                ret = False
                                return license_plate_text
                            
    finally:
        if 'cap' in locals() and cap.isOpened():
            cap.release()


