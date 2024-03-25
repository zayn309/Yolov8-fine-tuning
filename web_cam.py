import argparse
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description="YOLOv8 Model Inference")
    parser.add_argument("--model_path", type=str, default="yolov8m", help="Path to the YOLOv8 model weights (default: yolov8m)")
    args = parser.parse_args()

    model = YOLO(args.model_path)
    results = model.predict(source='0', show=True)
    print(results)

if __name__ == "__main__":
    main()

"""
Example usage:
    python web_cam.py --model_path /path/to/your/model.weights
"""
