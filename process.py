import cv2
import tkinter as tk
from PIL import ImageTk, Image
import os
import numpy as np 

# Define image processing functions
def blur_image(image):
    blurred_image = cv2.GaussianBlur(image, (15, 15), 0)
    return blurred_image

def apply_night_mode(image):
    inverted_image = cv2.bitwise_not(image)
    return inverted_image

def adjust_brightness(image, value):
    adjusted_image = np.clip(image + value, 0, 255).astype(np.uint8)
    return adjusted_image

def sharpen_image(image, value):
    sharpened_image = cv2.filter2D(image, -1, np.array([[-1, -1, -1],
                                                        [-1,  9 + value, -1],
                                                        [-1, -1, -1]]))
    return sharpened_image

def detect_edges(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 90, 180)
    edge_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return edge_image

# Function to display the processed image
def display_image(image):
    img = Image.fromarray(image)
    img = ImageTk.PhotoImage(img)
    panel.configure(image=img)
    panel.image = img

def open_file():
    global image_paths, current_image_index, image, original_image
    try:
        if image_paths:
            file_path = image_paths[current_image_index]
            image = cv2.imread(file_path)
            if image is not None:
                original_image = image.copy()
                processed_image = process_image('Original')
                if processed_image is not None:
                    display_image(processed_image)
            else:
                print("Error loading image.")
            current_image_index = (current_image_index + 1) % len(image_paths)
        else:
            print("No more images to load.")
    except Exception as e:
        print("Error opening file:", e)

def process_image(option):
    global image, original_image
   
    if option == 'Original':
            processed_image = original_image
    elif option == 'Blur':
            processed_image = blur_image(image)
    elif option == 'Night Mode':
            processed_image = apply_night_mode(image)
    elif option == 'Brightness+':
            processed_image = adjust_brightness(image, 50)
    elif option == 'Brightness-':
            processed_image = adjust_brightness(image, -50)
    elif option == 'Sharpen+':
            processed_image = sharpen_image(image, 1)
    elif option == 'Sharpen-':
            processed_image = sharpen_image(image, -1)
    elif option == 'Edge Detection':
            processed_image = detect_edges(image)
    if processed_image is not None:
            display_image(processed_image)
   

# Create a Tkinter window
root = tk.Tk()
root.title("Image Processing")

# Create a frame for the buttons and pack it on the left side
button_frame = tk.Frame(root)
button_frame.pack(side=tk.LEFT, padx=5, pady=5)

# Create buttons for different options
options = ['Original', 'Blur', 'Night Mode', 'Brightness+', 'Brightness-', 'Sharpen+', 'Sharpen-', 'Edge Detection']
for option in options:
    button = tk.Button(button_frame, text=option, command=lambda option=option: process_image(option))
    button.pack(side=tk.TOP, padx=5, pady=5)

# Create a button to choose images
choose_button = tk.Button(button_frame, text="Next Image", command=open_file)
choose_button.pack(side=tk.TOP, padx=5, pady=5)

# Load images from the "image" folder
def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.tiff')):
            images.append(os.path.join(folder_path, filename))
    return images

image_folder_path = "image"
image_paths = load_images_from_folder(image_folder_path)
image = None
original_image = None

# Create a panel to display images
panel = tk.Label(root)
panel.pack()

# Initialize current_image_index
current_image_index = 0

# Display the first image when the Tkinter window opens
open_file()

# Run the Tkinter event loop
root.mainloop()
