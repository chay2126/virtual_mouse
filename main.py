import cv2
from hand_tracking.hand_tracker import HandTracker


def main():

    cap = cv2.VideoCapture(0)

    tracker = HandTracker()

    while True:

        success, frame = cap.read()

        frame = cv2.flip(frame, 1)

        frame, landmarks = tracker.detect_hands(frame)

        if landmarks:

            fingers = tracker.get_fingers_up(landmarks)

            print(fingers)

        cv2.imshow("Virtual Mouse - Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()