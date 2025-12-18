from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

image_photo = None              # Original uploaded image   
display_image = None            # Display version of uploaded image\

watermark_photo = None          # Original uploaded watermark    
display_watermark = None        # Display version of uploaded watermark

# Flags to verify uploads
image_uploaded = False
watermark_uploaded = False

# Variables for result image and preview window
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
        wtm = Image.open(watermark_path).convert("RGBA")
        watermark_photo = wtm
        display_wtm = wtm.copy()
        display_wtm.thumbnail((280, 400))
        display_watermark = ImageTk.PhotoImage(display_wtm)

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
        convert.pack(pady=10)

def save_image():
    global result_image
    if result_image:
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")]
        )
        if save_path.endswith(('.jpg', '.jpeg')):
            result_image.convert("RGB").save(save_path)
        else:
            result_image.save(save_path)

def show_preview_window():
    global result_image, display_result, preview_window
    if preview_window is None or not preview_window.winfo_exists():
        # Create a new preview window
        preview_window = tk.Toplevel()
        preview_window.title("Watermarked Image Preview")
        preview_window.minsize(550,450)
        preview_window.resizable(False, False)

        # Identify position of root window to align preview window
        root_x = window.winfo_x()
        root_y = window.winfo_y()
        main_width = window.winfo_width()
        gap = 20
        preview_window.geometry(f"+{root_x + main_width + gap}+{root_y}")

        # Create a frame to hold the preview image and save button
        preview_frame = tk.Frame(preview_window)
        preview_frame.pack(fill="both", expand=True, padx=10)

        # Canvas to display preview image
        preview_window.canvas = tk.Canvas(preview_frame, width= 500, height=400, bg="lightgray")
        preview_window.canvas.pack()

        # Create a frame for rotation buttons and save button
        button_frame = tk.Frame(preview_frame)
        button_frame.pack(pady=10)
        
        # Left rotation button
        rotate_result_left = tk.Button(
            button_frame,
            text="⬅️",
            command=lambda: rotate_image('result', -90),
            font=("Arial", 12),
            width=3,
        )
        rotate_result_left.pack(side="left", padx=5)
        
        # Save button
        save_img = tk.Button(button_frame, text="Save", command=save_image)
        save_img.pack(side="left", padx=5)
        
        # Right rotation button
        rotate_result_right = tk.Button(
            button_frame,
            text="➡️",
            command=lambda: rotate_image('result', 90),
            font=("Arial", 12),
            width=3,
        )
        rotate_result_right.pack(side="left", padx=5)

    preview = result_image.copy()
    preview.thumbnail((500, 400))
    display_result = ImageTk.PhotoImage(preview)

    preview_window.canvas.delete("all")
    preview_window.canvas.create_image(250, 200, image=display_result)



def add_watermark():
    global image_photo, watermark_photo, result_image, display_result
    print(image_photo, watermark_photo)

    if image_photo and watermark_photo:
        try:
            # Scale based on image area
            image_area = image_photo.width * image_photo.height
            target_watermark_area = image_area * 0.05

            watermark_area = watermark_photo.width * watermark_photo.height
            scale_factor = (target_watermark_area / watermark_area) ** 0.5

            watermark_width = int(watermark_photo.width * scale_factor)
            watermark_height = int(watermark_photo.height * scale_factor)

            max_width = int(image_photo.width * 0.3)
            max_height = int(image_photo.height * 0.3)

            if watermark_width > max_width or watermark_height > max_height:
                width_ratio = max_width / watermark_width
                height_ratio = max_height / watermark_height
                min_ratio = min(width_ratio, height_ratio)
                watermark_width = int(watermark_width * min_ratio)
                watermark_height = int(watermark_height * min_ratio)

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
            show_preview_window()

        except:
            return "Error applying watermark"

def rotate_image(type, degrees):
    global image_photo, display_image, watermark_photo, display_watermark, result_image, display_result, preview_window
    if type == 'image':
        if image_photo is None:
            return
        image_photo = image_photo.rotate(-degrees, expand=True)
        display_img = image_photo.copy()
        display_img.thumbnail((280, 400))
        display_image = ImageTk.PhotoImage(display_img)

        image_canvas.delete("all")
        image_canvas.create_image(140, 200, image=display_image)
    
    elif type == 'watermark':
        if watermark_photo is None:
            return
        watermark_photo = watermark_photo.rotate(-degrees, expand=True)
        display_wtm = watermark_photo.copy()
        display_wtm.thumbnail((280, 400))
        display_watermark = ImageTk.PhotoImage(display_wtm)

        watermark_canvas.delete("all")
        watermark_canvas.create_image(140, 200, image=display_watermark)
    
    elif type == 'result':
        if result_image is None:
            return
        result_image = result_image.rotate(-degrees, expand=True)
        preview = result_image.copy()
        preview.thumbnail((500, 400))
        display_result = ImageTk.PhotoImage(preview)

        if preview_window and preview_window.winfo_exists():
            preview_window.canvas.delete("all")
            preview_window.canvas.create_image(250, 200, image=display_result)

window = tk.Tk()
window.title("Image Watermark Generator")
window.minsize(600,500)
window.resizable(False, False)


# Create a main frame to display upload buttons and canvases
frames_container = tk.Frame(window)
frames_container.pack(fill="both", expand=False)

# Create left and right frames for image and watermark
left_frame = tk.Frame(frames_container)
left_frame.pack(side="left", fill="both", expand=True, padx=10)
right_frame = tk.Frame(frames_container)
right_frame.pack(side="right", fill="both", expand=True, padx=10)

uploaded_image = tk.Button(left_frame, text="image", command=upload_image)           # Upload Image Button
uploaded_image.pack()
image_canvas = tk.Canvas(left_frame, width=280, height=400, bg="lightgray")              # Canvas to display uploaded image
image_canvas.pack(pady=10)

image_rotate_frame = tk.Frame(left_frame)
image_rotate_frame.pack(pady=5)
rotate_image_left = tk.Button(
    image_rotate_frame,
    text="⬅️",
    command=lambda: rotate_image('image', -90),
    font=("Arial", 12),
    width=3,
)
rotate_image_left.pack(side="left", padx=5)         # Rotate Left Button
rotate_image_right = tk.Button(
    image_rotate_frame,
    text="➡️",
    command=lambda: rotate_image('image', 90),
    font=("Arial", 12),
    width=3,
)
rotate_image_right.pack(side="left", padx=5)         # Rotate Right Button

uploaded_watermark = tk.Button(right_frame, text="watermark", command=upload_watermark)           # Upload Watermark Button
uploaded_watermark.pack()
watermark_canvas = tk.Canvas(right_frame, width=280, height=400, bg="lightgray")              # Canvas to display uploaded watermark
watermark_canvas.pack(pady=10)
watermark_rotate_frame = tk.Frame(right_frame)
watermark_rotate_frame.pack(pady=5)
rotate_watermark_left = tk.Button(
    watermark_rotate_frame,
    text="⬅️",
    command=lambda: rotate_image('watermark', -90),
    font=("Arial", 12),
    width=3,
)
rotate_watermark_left.pack(side="left", padx=5)         # Rotate Left Button
rotate_watermark_right = tk.Button(
    watermark_rotate_frame,
    text="➡️",
    command=lambda: rotate_image('watermark', 90),
    font=("Arial", 12),
    width=3,
)
rotate_watermark_right.pack(side="left", padx=5)         # Rotate Right Button

# Hide convert button initially, will be displayed after both uploads verified
convert = tk.Button(window, text="Apply Watermark", command=add_watermark)

window.mainloop()
