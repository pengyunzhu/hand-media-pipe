import math


class GestureClassifier:
    """簡單手勢分類器，使用 MediaPipe 手部關鍵點進行規則式判斷。"""

    def __init__(self):
        self.tip_ids = [4, 8, 12, 16, 20]

    def _finger_open(self, lm_list, finger_idx, hand_label):
        """判斷單一手指是否為打開狀態。"""
        if not lm_list:
            return False

        tip_id = self.tip_ids[finger_idx]
        pip_id = tip_id - 2

        if finger_idx == 0:
            # 拇指使用左右手方向判斷
            if hand_label == 'Right':
                return lm_list[tip_id][1] > lm_list[pip_id][1]
            else:
                return lm_list[tip_id][1] < lm_list[pip_id][1]
        return lm_list[tip_id][2] < lm_list[pip_id][2]

    def _distance(self, a, b):
        """計算兩點之間的歐式距離。"""
        return math.hypot(a[1] - b[1], a[2] - b[2])

    def classify(self, lm_list, hand_label='Right'):
        """根據手指開/合狀態，回傳手勢名稱與顯示文字。"""
        if not lm_list:
            return 'No Gesture'

        finger_states = [self._finger_open(lm_list, idx, hand_label) for idx in range(5)]
        thumb, index, middle, ring, pinky = finger_states

        # 判斷手勢
        if index and middle and ring and pinky and thumb:
            return 'Open Palm'  # 張開手掌

        if not index and not middle and not ring and not pinky and thumb:
            # 拇指向上需確認手腕方向
            thumb_tip = lm_list[4]
            wrist = lm_list[0]
            if thumb_tip[2] < wrist[2]:
                return 'Thumbs Up'  # 👍

        if not thumb and not index and not middle and not ring and not pinky:
            return 'Fist'  # 拳頭

        if index and not middle and not ring and not pinky:
            return 'Pointing Up'  # 食指

        if index and middle and not ring and not pinky:
            return 'Victory'  # YA

        return 'Unknown Gesture'

    def get_action(self, gesture_name):
        """取得手勢對應的功能文字。"""
        mapping = {
            'Thumbs Up': '音量增加',
            'Open Palm': '暫停影片／停止',
            'Fist': '關閉功能',
            'Pointing Up': '下一頁',
            'Victory': '播放影片',
        }
        return mapping.get(gesture_name, '無對應功能')
