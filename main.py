import cv2
import pyautogui
from hand_tracking.hand_tracker import HandTracker


def main():

    cap = cv2.VideoCapture(0)

    tracker = HandTracker()

    screen_w, screen_h = pyautogui.size()

    while True:

        success, frame = cap.read()

        frame = cv2.flip(frame, 1)

        frame, landmarks = tracker.detect_hands(frame)

        if landmarks:

            fingers = tracker.get_fingers_up(landmarks)

            # index finger tip
            x = landmarks[8][1]
            y = landmarks[8][2]

            frame_h, frame_w, _ = frame.shape

            screen_x = int(x * screen_w / frame_w)
            screen_y = int(y * screen_h / frame_h)

            if fingers[1] == 1 and fingers[2] == 0:
                pyautogui.moveTo(screen_x, screen_y)

            print(fingers)

        cv2.imshow("Virtual Mouse - Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()