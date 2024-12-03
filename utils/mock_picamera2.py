# mock_picamera2.py

class Picamera2:
    def __init__(self):
        print("Mock Picamera2 initialized")

    def start_preview(self):
        print("Mock: start_preview called")

    def stop_preview(self):
        print("Mock: stop_preview called")

    def capture(self, output, format="jpeg"):
        print(f"Mock: Capturing image to {output} with format {format}")

    def start_recording(self, output):
        print(f"Mock: Recording started to {output}")

    def stop_recording(self):
        print("Mock: Recording stopped")

    # Add any additional methods you need to mock
