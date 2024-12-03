from flask import Flask, render_template, Response, jsonify
import torch
import time
import pathlib
import os
import glob
import cv2
import numpy as np
from flask_cors import CORS
from pathlib import Path
from io import BytesIO
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

app = Flask(__name__)
CORS(app)
# 경로 수정
temp = pathlib.PosixPath
pathlib.WindowsPath = pathlib.PosixPath

# YOLOv5 모델 로드
model_path = Path("/home/pi/yolov5/final_best.pt")
model = torch.hub.load('ultralytics/yolov5', 'custom', path=str(model_path), force_reload=True)

# 시간 및 경고 변수
last_snapshot_time = 0
snapshot_interval = 10
alert_status = {'alert': False}
object_size_percentage = 0

snapshots_dir = "static/snapshots"
os.makedirs(snapshots_dir, exist_ok=True)

# 시작 시 스냅샷 폴더 비우기
def clear_snapshots(directory):
    files = glob.glob(f'{directory}/*')
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            print(f"Error deleting file {f}: {e}")

clear_snapshots(snapshots_dir)

# Picamera2 초기화
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.encoder = JpegEncoder()
picam2.output = FileOutput()

# 카메라 시작
picam2.start()

# 프레임 생성 함수 수정
def gen_frames():
    global object_size_percentage, last_snapshot_time
    while True:
        buffer = BytesIO()
        picam2.capture_file(buffer, format='jpeg')
        buffer.seek(0)
        frame = cv2.imdecode(np.frombuffer(buffer.read(), np.uint8), cv2.IMREAD_COLOR)

        try:
            results = model(frame)
            total_box_size = 0
            frame_size = frame.shape[0] * frame.shape[1]

            for *xyxy, conf, cls in results.xyxy[0]:
                class_name = model.names[int(cls)]
                x1, y1, x2, y2 = map(int, xyxy)
                box_width = x2 - x1
                box_height = y2 - y1
                box_size = box_width * box_height
                total_box_size += box_size

                label = f'{class_name} {conf:.2f}'
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            object_size_percentage = (total_box_size / frame_size)  if frame_size > 0 else 0

            if any(model.names[int(cls)] in ['Phone', 'Wallet'] for *xyxy, conf, cls in results.xyxy[0]):
                current_time = time.time()
                if current_time - last_snapshot_time >= snapshot_interval:
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    current_time_text = time.strftime("%Y-%m-%d %H:%M:%S")
                    cv2.putText(frame, f'{current_time_text}', (10, frame.shape[0] - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.imwrite(f'{snapshots_dir}/{timestamp}.jpg', frame)
                    cv2.putText(frame, f'Snapshot taken at {timestamp}', (10, frame.shape[0] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                    last_snapshot_time = current_time

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"Error processing frame: {e}")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 나머지 라우트는 변경되지 않음
@app.route('/alert', methods=['GET'])
def get_alert():
    return jsonify(alert_status)

@app.route('/object_size', methods=['GET'])
def get_object_size():
    return jsonify({'size_percentage': object_size_percentage})

@app.route('/')
def index():
    snapshots = sorted(os.listdir(snapshots_dir), reverse=True)
    snapshot_info = [{'filename': filename, 'timestamp': filename.split('.')[0]} for filename in snapshots]
    return render_template('index.html', snapshot_info=snapshot_info)

@app.route('/snapshots')
def get_snapshots():
    snapshots = sorted(os.listdir(snapshots_dir), reverse=True)
    snapshot_list = [{'path': f'/static/snapshots/{filename}', 'timestamp': filename} for filename in snapshots]
    return jsonify(snapshot_list)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
