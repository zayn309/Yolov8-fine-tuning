"""
The path could be an image or an mp4 video
"""

import argparse
from ultralytics import YOLO

def main(image_path, confidence_threshold, model_path='yolov8m.pt'):
    model = YOLO(model_path)
    results = model.predict(source=image_path, conf=confidence_threshold, save=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='YOLO Object Detection')
    parser.add_argument('image_path', type=str, help='Path to the input image')
    parser.add_argument('--confidence', type=float, default=0.25, help='Confidence threshold (default: 0.25)')
    parser.add_argument('--model', type=str, default='yolov8m.pt', help='Path to the YOLO model (default: yolov8m.pt)')
    args = parser.parse_args()

    main(args.image_path, args.confidence, args.model)

"""
Example:
    python your_script.py path/to/your/image.jpg --confidence 0.3 --model yolov8m.pt
"""
