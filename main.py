from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

from sympy import preview

image_photo = None
display_image = None
watermark_photo = None
display_watermark = None
image_uploaded = False
watermark_uploaded = False
result_image = None
display_result = None
preview_window = None
def upload_image():
    global image_photo, image_uploaded, display_image

    # User selects an image file
    image_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg")]
    )
    if image_path:
        img = Image.open(image_path)
        image_photo = img.convert("RGBA")
        img.thumbnail((280, 400))
        display_image = ImageTk.PhotoImage(img)

        # Display the uploaded image in the canvas
        image_canvas.delete("all")
        image_canvas.create_image(140, 200, image=display_image)

        # If image is uploaded, verify uploads to display convert button
        image_uploaded = True
        verify_uploads()
    else:
        print("No image selected")


def upload_watermark():
    global watermark_photo, watermark_uploaded, display_watermark

    # User selects a watermark file
    watermark_path = filedialog.askopenfilename(
        title="Select a watermark",
        filetypes=[("Image files", "*.png *.jpg *.jpeg")]
    )
    if watermark_path:
        wtm = Image.open(watermark_path)
        watermark_photo = wtm.convert("RGBA")
        wtm.thumbnail((280, 400))
        display_watermark = ImageTk.PhotoImage(wtm)

        # Display the uploaded watermark in the canvas
        watermark_canvas.delete("all")
        watermark_canvas.create_image(140, 200, image=display_watermark)

        # If watermark is uploaded, verify uploads to display convert button
        watermark_uploaded = True
        verify_uploads()
    else:
        print("No watermark selected")

def verify_uploads():
    if image_uploaded and watermark_uploaded:
        convert.pack(pady=20)

def save_image():
    global result_image
    if result_image:
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")]
        )
        if save_path:
            result_image.save(save_path)

def show_preview_window():
    global result_image, display_result, preview_window
    if not preview_window or not preview_window.winfo_exists():
        preview_window = tk.Toplevel()
        preview_window.title("Watermarked Image Preview")
        preview_window.minsize(600,550)
        preview_window.resizable(False, False)
        preview_frame = tk.Frame(preview_window)
        preview_frame.pack(fill="both", expand=True, padx=10)
        preview_canvas = tk.Canvas(preview_frame, width=560, height=500, bg="lightgray")
        preview_canvas.pack(pady=10)
        preview_canvas.create_image(280, 250, image=display_result)
        save_img = tk.Button(preview_frame, text="Save", command=save_image)
        save_img.pack(pady=10)


def add_watermark():
    global image_photo, watermark_photo, result_image, display_result
    print(image_photo, watermark_photo)

    if image_photo and watermark_photo:
        try:
            # Resize watermark to 30% of the image width
            watermark_width = int(image_photo.width * 0.3)
            watermark_height = int(watermark_photo.height * (watermark_width / watermark_photo.width))
            resized_watermark = watermark_photo.resize((watermark_width, watermark_height))

            # Position watermark at bottom-right corner
            margin = 10
            position = (image_photo.width - watermark_width - margin,       # X position from left
                        image_photo.height - watermark_height - margin)     # Y position from top

            # Create a transparent layer same size as original image, and paste watermark onto it
            transparent_layer = Image.new('RGBA', image_photo.size, (0,0,0,0))
            transparent_layer.paste(resized_watermark, position, resized_watermark)

            # Combine original image with watermark layer
            result = Image.alpha_composite(image_photo, transparent_layer)
            result_image = result
            result.thumbnail((560, 400))
            display_result = ImageTk.PhotoImage(result)
            show_preview_window()

        except:
            return "Error applying watermark"


window = tk.Tk()
window.title("Image Watermark Generator")
window.minsize(600,550)
window.resizable(False, False)


# Create a main frame to display upload buttons and canvases
frames_container = tk.Frame(window)
frames_container.pack(fill="both", expand=False)

# Create left and right frames for image and watermark
left_frame = tk.Frame(frames_container)
left_frame.pack(side="left", fill="both", expand=True, padx=10)
right_frame = tk.Frame(frames_container)
right_frame.pack(side="right", fill="both", expand=True, padx=10)

uploaded_image = tk.Button(left_frame, text="Upload Image", command=upload_image)           # Upload Image Button
uploaded_image.pack(pady=10)
image_canvas = tk.Canvas(left_frame, width=280, height=400, bg="lightgray")              # Canvas to display uploaded image
image_canvas.pack(pady=10)

uploaded_watermark = tk.Button(right_frame, text="Upload Watermark", command=upload_watermark)           # Upload Watermark Button
uploaded_watermark.pack(pady=10)
watermark_canvas = tk.Canvas(right_frame, width=280, height=400, bg="lightgray")              # Canvas to display uploaded watermark
watermark_canvas.pack(pady=10)

# Hide convert button initially, will be displayed after both uploads verified
convert = tk.Button(window, text="Apply Watermark", command=add_watermark)

window.mainloop()
