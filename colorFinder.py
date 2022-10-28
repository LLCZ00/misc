#used for finding HSV color ranges/creating masks for color detection in openCV

import cv2
import numpy as np


def empty(ass):
    pass


def track_bars():
    cv2.namedWindow('Color Track')
    cv2.resizeWindow('Color Track', 640, 240)

    cv2.createTrackbar('Hue min', 'Color Track', 0, 179, empty)
    cv2.createTrackbar('Hue max', 'Color Track', 179, 179, empty)
    cv2.createTrackbar('Sat min', 'Color Track', 0, 255, empty)
    cv2.createTrackbar('Sat max', 'Color Track', 255, 255, empty)
    cv2.createTrackbar('Val min', 'Color Track', 0, 255, empty)
    cv2.createTrackbar('Val max', 'Color Track', 255, 255, empty)


def color_values(frame, win_name='Color Track'):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(hsv, (5, 5), 0)

    h_min = cv2.getTrackbarPos("Hue min", win_name)
    h_max = cv2.getTrackbarPos("Hue max", win_name)

    s_min = cv2.getTrackbarPos("Sat min", win_name)
    s_max = cv2.getTrackbarPos("Sat max", win_name)

    v_min = cv2.getTrackbarPos("Val min", win_name)
    v_max = cv2.getTrackbarPos("Val max", win_name)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    return cv2.inRange(blur, lower, upper)  # Returns mask


def main():
    cap = cv2.VideoCapture(1)
    track_bars()  # initiates trackbar window

    while True:
        _, frame = cap.read()

        cv2.imshow('og', frame)
        cv2.imshow('mask', color_values(frame))

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
