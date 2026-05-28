# AI 即時手勢辨識智慧控制系統

這是一個使用 Python、OpenCV 與 MediaPipe Hands 製作的即時手勢辨識專題示範程式。系統會透過電腦攝影機即時監測手部姿勢，辨識常見手勢並執行對應功能。

## 功能說明

- 即時顯示攝影機畫面
- 使用 MediaPipe Hands 偵測手部骨架與手指節點
- 支援 5 種手勢辨識：
  - 👍：音量增加
  - ✋：暫停影片／停止
  - ✊：關閉功能
  - ☝️：下一頁
  - ✌️：播放影片
- 畫面上顯示：手部骨架、手勢名稱、執行功能、FPS
- 手勢需維持約 1 秒才觸發功能，避免連續誤判

## 專案結構

- `main.py`：主程式，負責相機讀取、畫面顯示與手勢觸發邏輯
- `hand_detector.py`：手部偵測模組，使用 MediaPipe Hands
- `gesture_classifier.py`：手勢分類模組，負責轉換骨架資訊為手勢名稱
- `utils.py`：工具函式，包含 FPS 計算與文字繪製
- `requirements.txt`：所需 Python 套件

## 安裝方式

```bash
pip install -r requirements.txt
```

## 執行方式

```bash
python main.py
```

按 `q` 離開程式。

## 注意事項

- 若系統無法執行 `pyautogui` 的音量或鍵盤控制，程式仍會正常顯示手勢與動作文字。
- 建議在良好光源與乾淨背景下進行手勢演示，辨識效果較佳。
