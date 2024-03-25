import argparse
from ultralytics import YOLO

def main(model_path):
    model = YOLO(model_path)
    model.train(data="./Dataset/data.yaml", epochs=50, amp=True, plots=True, close_mosaic=15)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train YOLOv8 model")
    parser.add_argument("model_path", type=str, help="Path to the YOLOv8 model configuration file")
    args = parser.parse_args()
    main(args.model_path)
