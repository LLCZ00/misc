import cv2, socket
import numpy as np

ip = '192.168.1.39'
port = 2390
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_data(data):
    s.sendto(data, (ip, port))


def get_contours(img, frame, datacontainer):
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for cunt in contours:
        area = cv2.contourArea(cunt)
        if area > 300:
            cv2.drawContours(frame, cunt, -1, (255, 0, 0), 3)  # draws outline of detected object
            peri = cv2.arcLength(cunt, False)
            approx = cv2.approxPolyDP(cunt, 0.05*peri, False)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.circle(frame, (x+w//2, y+h//2), 5, (255, 0, 0), 3)  # Puts circle in center of object

            data = f'x{(x+w//2)+65}y{(y+h//2)}'  # data to be sent
            # "function" to avoid sending the same coordinates over and over
            if len(datacontainer) == 0:
                send_data(bytes(data, 'utf-8'))
            elif data in datacontainer:
                pass
            elif data not in datacontainer:
                send_data(bytes(data, 'utf-8'))
                datacontainer = []



def main(vidcap=0):
    cap = cv2.VideoCapture(vidcap)
    lower, upper = np.array([164, 20, 86]), np.array([179, 161, 255])  # pink balloon values (takes shine into account)
    data = []

    while True:
        _, frame = cap.read()
        hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blur = cv2.GaussianBlur(hsvframe, (5, 5), 0)
        mask = cv2.inRange(blur, lower, upper)

        get_contours(mask, frame, data)

        cv2.imshow('balloons', frame)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(1)
