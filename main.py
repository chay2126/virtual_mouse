import cv2
import pyautogui
import time
from hand_tracking.hand_tracker import HandTracker


def main():

    cap = cv2.VideoCapture(0)

    tracker = HandTracker()

    screen_w, screen_h = pyautogui.size()

    smoothening = 7
    prev_x, prev_y_cursor = 0, 0

    last_click_time = 0
    click_delay = 0.5

    last_right_click_time = 0
    right_click_delay = 0.5

    prev_y = 0
    dragging = False

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
                curr_x = prev_x + (screen_x - prev_x) / smoothening
                curr_y = prev_y_cursor + (screen_y - prev_y_cursor) / smoothening

                pyautogui.moveTo(curr_x, curr_y)

                prev_x, prev_y_cursor = curr_x, curr_y
            # thumb and index coordinates
            thumb = (landmarks[4][1], landmarks[4][2])
            index = (landmarks[8][1], landmarks[8][2])

            distance = tracker.find_distance(thumb, index)

            current_time = time.time()

            # drag gesture
            if distance < 30:

                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True

            else:

                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

            # middle and index coordinates
            index = (landmarks[8][1], landmarks[8][2])
            middle = (landmarks[12][1], landmarks[12][2])

            distance_im = tracker.find_distance(index, middle)

            if distance_im < 30 and current_time - last_right_click_time > right_click_delay and fingers[2] == 1:
                pyautogui.rightClick()
                last_right_click_time = current_time

            # scroll gesture (index + pinky)
            if fingers[1] == 1 and fingers[4] == 1 and fingers[2] == 0 and fingers[3] == 0:

                current_y = landmarks[8][2]

                if prev_y != 0:

                    if current_y - prev_y > 15:
                        pyautogui.scroll(-40)

                    elif prev_y - current_y > 15:
                        pyautogui.scroll(40)

                prev_y = current_y

            else:
                prev_y = 0     

        cv2.imshow("Virtual Mouse - Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()