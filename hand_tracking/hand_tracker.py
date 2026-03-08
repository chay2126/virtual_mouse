import cv2
import mediapipe as mp
import math

class HandTracker:

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.mp_draw = mp.solutions.drawing_utils

    def detect_hands(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        landmarks = []

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                for id, lm in enumerate(hand_landmarks.landmark):

                    h, w, c = frame.shape

                    cx = int(lm.x * w)
                    cy = int(lm.y * h)

                    landmarks.append((id, cx, cy))

        return frame, landmarks
    
    def get_fingers_up(self, landmarks):

        fingers = []

        # Thumb
        if landmarks[4][1] > landmarks[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Index
        if landmarks[8][2] < landmarks[6][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Middle
        if landmarks[12][2] < landmarks[10][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Ring
        if landmarks[16][2] < landmarks[14][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Pinky
        if landmarks[20][2] < landmarks[18][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        return fingers
    
    def find_distance(self, p1, p2):

        x1, y1 = p1
        x2, y2 = p2

        distance = math.hypot(x2 - x1, y2 - y1)

        return distance