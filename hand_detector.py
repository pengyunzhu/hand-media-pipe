import cv2
import mediapipe as mp


class HandDetector:
    """使用 MediaPipe Hands 進行手部偵測與關鍵點取得。"""

    def __init__(self, max_num_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.max_num_hands = max_num_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, image, draw=True):
        """偵測手部，並可選擇在圖片上繪製手部骨架。"""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image_rgb)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        image,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                        self.mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2),
                    )
        return image

    def find_position(self, image, hand_no=0):
        """取得指定手的手指座標資料，並回傳手勢左右手標籤。"""
        lm_list = []
        hand_label = None
        if self.results is None or not self.results.multi_hand_landmarks:
            return lm_list, hand_label

        if hand_no < len(self.results.multi_hand_landmarks):
            hand_landmarks = self.results.multi_hand_landmarks[hand_no]
            h, w, _ = image.shape
            for idx, landmark in enumerate(hand_landmarks.landmark):
                lm_list.append([
                    idx,
                    int(landmark.x * w),
                    int(landmark.y * h),
                    landmark.z,
                ])

            if self.results.multi_handedness:
                hand_label = self.results.multi_handedness[hand_no].classification[0].label

        return lm_list, hand_label
