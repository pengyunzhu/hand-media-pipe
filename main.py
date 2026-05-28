import time
import cv2
import pyautogui

from hand_detector import HandDetector
from gesture_classifier import GestureClassifier
from utils import draw_text, FpsCounter


def perform_action(gesture_name, status):
    """執行對應手勢功能，並回傳目前顯示的動作文字。"""
    try:
        if gesture_name == 'Thumbs Up':
            # 嘗試調整系統音量，並保留文字提示
            pyautogui.press('volumeup')
            return '音量增加'
        if gesture_name == 'Open Palm':
            pyautogui.press('space')
            return '暫停影片／停止'
        if gesture_name == 'Fist':
            return '關閉功能'
        if gesture_name == 'Pointing Up':
            pyautogui.press('right')
            return '下一頁'
        if gesture_name == 'Victory':
            pyautogui.press('space')
            return '播放影片'
    except Exception:
        # 如果 pyautogui 操作失敗，僅顯示文字說明
        return status
    return status


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    detector = HandDetector(max_num_hands=1, detection_confidence=0.7, tracking_confidence=0.7)
    classifier = GestureClassifier()
    fps_counter = FpsCounter()

    stable_gesture = None
    gesture_start_time = 0
    last_triggered_gesture = None
    last_triggered_time = 0
    current_action = '等待手勢...' 
    hint_text = '請將手放在鏡頭前，並保持動作 1 秒。'

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        frame = detector.find_hands(frame, draw=True)
        lm_list, hand_label = detector.find_position(frame)

        gesture_name = 'No Gesture'
        if lm_list:
            gesture_name = classifier.classify(lm_list, hand_label or 'Right')

        # 如果手勢穩定超過 1 秒，才觸發功能
        if gesture_name != stable_gesture:
            stable_gesture = gesture_name
            gesture_start_time = time.time()
        else:
            elapsed = time.time() - gesture_start_time
            if gesture_name not in ['No Gesture', 'Unknown Gesture'] and elapsed >= 1.0:
                if gesture_name != last_triggered_gesture or (time.time() - last_triggered_time) > 1.5:
                    current_action = perform_action(gesture_name, classifier.get_action(gesture_name))
                    last_triggered_gesture = gesture_name
                    last_triggered_time = time.time()
                    hint_text = f'已觸發：{current_action}'

        fps = fps_counter.update()

        draw_text(frame, f'FPS: {fps:.1f}', position=(10, 30), color=(0, 255, 255), scale=0.8)
        draw_text(frame, f'手勢: {gesture_name}', position=(10, 60), color=(255, 255, 0), scale=0.8)
        draw_text(frame, f'功能: {current_action}', position=(10, 95), color=(0, 255, 0), scale=0.8)
        draw_text(frame, f'提示: {hint_text}', position=(10, 130), color=(255, 255, 255), scale=0.7)

        cv2.imshow('AI 即時手勢辨識智慧控制系統', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
