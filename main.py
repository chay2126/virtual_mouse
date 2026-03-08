import cv2
import pyautogui
import time
from hand_tracking.hand_tracker import HandTracker


def main():

    cap = cv2.VideoCapture(0)

    tracker = HandTracker()

    screen_w, screen_h = pyautogui.size()

    last_click_time = 0
    click_delay = 0.5

    last_right_click_time = 0
    right_click_delay = 0.5

    while True:

        success, frame = cap.read()

        frame = cv2.flip(frame, 1)

        frame, landmarks = tracker.detect_hands(frame)

        if landmarks:

            fingers = tracker.get_fingers_up(landmarks)

            # index finger position
            x = landmarks[8][1]
            y = landmarks[8][2]

            frame_h, frame_w, _ = frame.shape

            screen_x = int(x * screen_w / frame_w)
            screen_y = int(y * screen_h / frame_h)

            # cursor movement
            if fingers[1] == 1 and fingers[2] == 0:
                pyautogui.moveTo(screen_x, screen_y)

            # thumb and index coordinates
            thumb = (landmarks[4][1], landmarks[4][2])
            index = (landmarks[8][1], landmarks[8][2])

            distance = tracker.find_distance(thumb, index)

            current_time = time.time()

            if distance < 30 and current_time - last_click_time > click_delay:
                pyautogui.click()
                last_click_time = current_time

            index = (landmarks[8][1], landmarks[8][2])
            middle = (landmarks[12][1], landmarks[12][2])

            distance_im = tracker.find_distance(index, middle)

            if distance_im < 30 and current_time - last_right_click_time > right_click_delay:
                pyautogui.rightClick()
                last_right_click_time = current_time    

        cv2.imshow("Virtual Mouse - Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()