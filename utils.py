import time
import cv2


def draw_text(image, text, position=(10, 30), color=(255, 255, 255), scale=0.7, thickness=2):
    """在畫面上繪製文字說明。"""
    cv2.putText(
        image,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        color,
        thickness,
        cv2.LINE_AA,
    )


class FpsCounter:
    """簡單 FPS 計算器。"""

    def __init__(self):
        self._last_time = time.time()
        self.fps = 0.0

    def update(self):
        current_time = time.time()
        delta = current_time - self._last_time
        if delta > 0:
            self.fps = 1.0 / delta
        self._last_time = current_time
        return self.fps
