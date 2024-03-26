import tkinter as tk
from tkinter import messagebox
from utils import parse_yaml, update_yaml
from tkinter import filedialog
import os
import shutil

def add_names_window():
    # Create names window
    names_window = tk.Toplevel(root)
    names_window.title("Add Names")
    data = parse_yaml()
    # Warning message
    warning_message = (f"Please make sure that your labels ID's start from {data['nc']},\n"
                       "the names are ordered above according to their IDs,\n"
                       "and the bbox coords follow the YOLO format.")
    
    # Display warning message
    messagebox.showwarning("Warning", warning_message)
    
    # Names frame
    names_frame = tk.Frame(names_window)
    names_frame.pack(padx=10, pady=10)
    
    # List to store name entry widgets
    name_entries = []
    
    def add_name_entry():
        name_frame = tk.Frame(names_frame)
        name_frame.pack(pady=5, anchor="w")
        name_entry = tk.Entry(name_frame, width=30)
        name_entry.pack(side="left")
        name_entries.append(name_entry)
    
    # Add initial name entry
    add_name_entry()
    
    # Add name button
    add_name_button = tk.Button(names_window, text="Add Name Entry", command=add_name_entry)
    add_name_button.pack()
    
    def close_window():
        # Get names from entry widgets
        names = [entry.get() for entry in name_entries]
        for name in names:
            data['names'].append(name)
        data['nc'] = data['nc'] + len(names)
        update_yaml(data)
        names_window.destroy()

    close_button = tk.Button(names_window, text="Close", command=close_window)
    close_button.pack(pady=10)


def add_data(image_path, label_path, valid_portion):
    # validate input paths
    if not os.path.exists(image_path) or not os.path.exists(label_path):
        print("Error: Invalid paths")
        return

    # Determine the number of images and calculate the number of images for validation
    num_images = len(os.listdir(image_path))
    num_valid_images = int(num_images * valid_portion)

    # Create valid directory if it doesn't exist
    valid_image_dir = os.path.join("./Dataset/valid/images")
    valid_label_dir = os.path.join("./Dataset/valid/labels")

    # print(num_images)
    # print(num_valid_images)
    # import sys
    # sys.exit(0)
    # Move data to valid and train directories
    num_copied_images = 0
    for i, img in enumerate(os.listdir(image_path)):
        img_path = os.path.join(image_path, img)
        label_file = os.path.join(label_path, img[:-3] + 'txt')
        if os.path.exists(label_file):  # Check if label file exists
            if i < num_valid_images:
                shutil.copy(img_path, os.path.join(valid_image_dir, img))
                shutil.copy(label_file, os.path.join(valid_label_dir, img.replace(".jpg", ".txt")))
            else:
                train_image_dir = os.path.join("./Dataset/train/images")
                train_label_dir = os.path.join("./Dataset/train/labels")
                shutil.copy(img_path, os.path.join(train_image_dir, img))
                shutil.copy(label_file, os.path.join(train_label_dir, img[:-3] + 'txt'))
            num_copied_images += 1
    print(f"{num_copied_images} images added to valid/train directories")

def get_paths_window(callback):
    def on_close():
        paths_window.destroy()

    def trigger_callback():
        # Extract data from entries
        image_path = image_entry.get()
        label_path = label_entry.get()
        valid_portion = valid_entry.get()

        # Check if any field is empty
        if not image_path or not label_path or not valid_portion:
            messagebox.showerror("Error", "Please fill in all the fields.")
            return

        # Check if valid_portion is a float
        try:
            valid_portion = float(valid_portion)
            if not 0 <= valid_portion <= 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Valid portion must be a float between 0.0 and 1.0.")
            return
        
        # Call the callback function with extracted data
        callback(image_path, label_path, valid_portion)
        paths_window.destroy()

    # Create paths window
    paths_window = tk.Toplevel(root)
    paths_window.title("Get Paths and Move Data")
    paths_window.protocol("WM_DELETE_WINDOW", on_close)
    
    # Main frame
    main_frame = tk.Frame(paths_window)
    main_frame.pack(padx=10, pady=10)
    
    # Warning label
    warning_label = tk.Label(paths_window, text="Please make sure that your labels' IDs start from the number of defined classes in data.yaml - 1", fg="red")
    warning_label.pack(side="top", fill="x")
    
    # Image path input
    image_frame = tk.Frame(main_frame)
    image_frame.pack(pady=(0, 5))
    image_label = tk.Label(image_frame, text="Image Path:")
    image_label.pack(side="left")
    image_entry = tk.Entry(image_frame, width=50)
    image_entry.pack(side="left")
    
    # Label path input
    label_frame = tk.Frame(main_frame)
    label_frame.pack(pady=(0, 5))
    label_label = tk.Label(label_frame, text="Label Path:")
    label_label.pack(side="left")
    label_entry = tk.Entry(label_frame, width=50)
    label_entry.pack(side="left")
    
    # Valid portion input
    valid_frame = tk.Frame(main_frame)
    valid_frame.pack(pady=(0, 5))
    valid_label = tk.Label(valid_frame, text="Valid Portion (0.0 - 1.0):")
    valid_label.pack(side="left")
    valid_entry = tk.Entry(valid_frame, width=10)
    valid_entry.pack(side="left")
    
    # Add data button
    add_button = tk.Button(main_frame, text="Add Data", command=trigger_callback)
    add_button.pack()

    # Close button
    close_button = tk.Button(main_frame, text="Close", command=on_close)
    close_button.pack()

# Create GUI window
root = tk.Tk()
root.title("Data Management")
root.geometry("400x200")  # Set window size

# Add names button
add_names_button = tk.Button(root, text="Add Names", command=add_names_window)
add_names_button.pack(pady=10)

# Get paths and move data button
get_paths_button = tk.Button(root, text="Get Paths and Move Data", command=lambda: get_paths_window(add_data))
get_paths_button.pack(pady=10)

root.mainloop()
