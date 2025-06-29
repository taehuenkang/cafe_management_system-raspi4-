# ☕ Cafe Management System – AI CCTV with YOLOv5 on Raspberry Pi

AI-enabled smart surveillance system designed for unmanned cafés.  
It detects spills, lost items (phone, wallet), and displays real-time monitoring.

---

## 📌 Project Overview

- 📷 Real-time object detection using **YOLOv5 (custom-trained)**  
- 🧪 Recognizes: `coffee_cup`, `wallet`, `phone`, `spills`  
- 🖥️ Web dashboard via **Flask** to display live video & status  
- 🍓 Hardware: **Raspberry Pi 4**, PiCamera2

---

## 🧰 Tech Stack

| Component     | Tools / Frameworks                      |
|---------------|------------------------------------------|
| AI Model      | YOLOv5 (PyTorch)                         |
| Backend       | Flask, OpenCV                            |
| Device        | Raspberry Pi 4, PiCamera2                |
| Labeling      | Roboflow, LabelImg                       |
| Language      | Python                                   |

---

## 🧠 Key Features

- 👁️ Live object detection streamed via Flask (MJPEG)
- 🧼 Spill detection with size threshold alert
- 🔒 Lost item snapshot auto-save (every 10s)
- 📦 Lightweight enough to run on Pi (option to scale to Jetson)

---

## 🖼️ Model Info

| Metric     | Value      |
|------------|------------|
| mAP@0.5    | 97.2%      |
| F1 Score   | 0.95       |
| Precision  | 99.6%      |
| Classes    | 4          |

---

## 🌐 Web Interface

- Displays bounding boxes with class labels
- Status panel for:
  - Detected spills
  - Saved snapshots with timestamps

---

## 🧪 How to Run

```bash
git clone https://github.com/SoCafeManager/Management-of-unmanned-cafes.git
cd cafe_project/
python3 app.py
