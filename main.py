import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageOps , ImageDraw
import matplotlib.pyplot as plt
import numpy as np

root = tk.Tk()
root.title("Image to Grayscale Converter")
root.geometry("900x600")
root.configure(bg="#2C3E50")

# عنوان اصلی
title_label = tk.Label(root, text="Image to Grayscale Converter", font=("Helvetica", 16, "bold"), fg="white", bg="#2C3E50")
title_label.pack(pady=10)

# فریم برای نمایش تصاویر
image_frame = tk.Frame(root, bg="#2C3E50")
image_frame.pack(pady=20)

# برچسب‌ها برای نمایش تصویر اصلی، grayscale، نگاتیو، و ترشولد
original_label_text = tk.Label(image_frame, text="Original Image", font=("Helvetica", 12), fg="white", bg="#2C3E50")
original_label_text.grid(row=0, column=0, padx=20)

grayscale_label_text = tk.Label(image_frame, text="Grayscale Image", font=("Helvetica", 12), fg="white", bg="#2C3E50")
grayscale_label_text.grid(row=0, column=1, padx=20)

negative_label_text = tk.Label(image_frame, text="Negative Image", font=("Helvetica", 12), fg="white", bg="#2C3E50")
negative_label_text.grid(row=0, column=2, padx=20)

threshold_label_text = tk.Label(image_frame, text="Threshold Image", font=("Helvetica", 12), fg="white", bg="#2C3E50")
threshold_label_text.grid(row=0, column=3, padx=20)

original_label = tk.Label(image_frame, bg="#34495E")
original_label.grid(row=1, column=0, padx=20, pady=10)

grayscale_label = tk.Label(image_frame, bg="#34495E")
grayscale_label.grid(row=1, column=1, padx=20, pady=10)

negative_label = tk.Label(image_frame, bg="#34495E")
negative_label.grid(row=1, column=2, padx=20, pady=10)

threshold_label = tk.Label(image_frame, bg="#34495E")
threshold_label.grid(row=1, column=3, padx=20, pady=10)

# متغیر برای ذخیره تصویر grayscale، نگاتیو و ترشولد
grayscale_image = None
negative_image = None
threshold_image = None

# تابع انتخاب تصویر
def select_image():
    global grayscale_image, negative_image, threshold_image  # برای دسترسی به متغیرهای grayscale و نگاتیو و ترشولد
    
    # باز کردن فایل
    file_path = filedialog.askopenfilename(
        filetypes=[("All Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif"), ("All Files", "*.*")]
    )
    
    if file_path:
        try:
            # بارگذاری و نمایش تصویر اصلی
            original_image = Image.open(file_path)
            original_image.thumbnail((200, 200))
            original_photo = ImageTk.PhotoImage(original_image)
            original_label.config(image=original_photo)
            original_label.image = original_photo
            
            # تبدیل تصویر به grayscale و نمایش
            grayscale_image = ImageOps.grayscale(original_image)
            grayscale_photo = ImageTk.PhotoImage(grayscale_image)
            grayscale_label.config(image=grayscale_photo)
            grayscale_label.image = grayscale_photo
            
            # ایجاد و نمایش تصویر نگاتیو
            negative_image = ImageOps.invert(grayscale_image)
            negative_photo = ImageTk.PhotoImage(negative_image)
            negative_label.config(image=negative_photo)
            negative_label.image = negative_photo

            # تنظیم ترشولد اولیه
            update_threshold(128)

        except Exception as e:
            print("Error loading image:", e)

# تابع نمایش هیستوگرام
def show_histogram(equalized=False):
    if grayscale_image is not None:
        # گرفتن داده‌های پیکسل‌های تصویر grayscale
        grayscale_data = np.array(grayscale_image)
        
        # چک کردن اینکه هیستوگرام نرمال‌سازی شده است یا خیر
        if equalized:
            # همسان‌سازی هیستوگرام
            grayscale_data = histogram_equalization(grayscale_data)
        
        # نمایش هیستوگرام در یک پنجره جدید
        hist_window = tk.Toplevel(root)
        hist_window.title("Grayscale Histogram (Equalized)" if equalized else "Grayscale Histogram")
        hist_window.geometry("500x400")
        hist_window.configure(bg="#2C3E50")
        
        # برچسب توضیحی
        hist_label = tk.Label(hist_window, text="Equalized Histogram" if equalized else "Original Histogram", font=("Helvetica", 14, "bold"), fg="white", bg="#2C3E50")
        hist_label.pack(pady=10)
        
        # رسم هیستوگرام با matplotlib
        fig, ax = plt.subplots(facecolor="#2C3E50")
        ax.hist(grayscale_data.ravel(), bins=256, range=(0, 255), color="#3498DB", alpha=0.85)
        ax.set_title("Pixel Intensity Distribution", color="white")
        ax.set_xlabel("Pixel Intensity", color="white")
        ax.set_ylabel("Frequency", color="white")
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        # جاسازی matplotlib در tkinter
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=hist_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        print("No grayscale image to display histogram.")

# تابع همسان‌سازی هیستوگرام
def histogram_equalization(image_array):
    # تبدیل به یک آرایه 1 بعدی و محاسبه هیستوگرام
    hist, bins = np.histogram(image_array.flatten(), bins=256, range=[0, 256], density=True)
    
    # محاسبه توزیع تجمعی (CDF)
    cdf = hist.cumsum()  
    cdf_normalized = 255 * cdf / cdf[-1]  # نرمال‌سازی
    
    # اعمال همسان‌سازی هیستوگرام
    image_equalized = np.interp(image_array.flatten(), bins[:-1], cdf_normalized)
    return image_equalized.reshape(image_array.shape).astype('uint8')

# تابع به‌روزرسانی ترشولد
def update_threshold(threshold_value):
    global threshold_image
    if grayscale_image is not None:
        # اعمال ترشولد
        threshold_data = np.array(grayscale_image)
        threshold_data = np.where(threshold_data > threshold_value, 255, 0).astype(np.uint8)
        threshold_image = Image.fromarray(threshold_data)
        
        # نمایش تصویر ترشولد شده
        threshold_photo = ImageTk.PhotoImage(threshold_image)
        threshold_label.config(image=threshold_photo)
        threshold_label.image = threshold_photo

# دکمه انتخاب تصویر
select_button = ttk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=10)

# دکمه نمایش هیستوگرام اصلی
histogram_button = ttk.Button(root, text="Show Original Histogram", command=lambda: show_histogram(equalized=False))
histogram_button.pack(pady=5)

# دکمه نمایش هیستوگرام متعادل‌شده
equalized_histogram_button = ttk.Button(root, text="Show Equalized Histogram", command=lambda: show_histogram(equalized=True))
equalized_histogram_button.pack(pady=5)

# اسلایدر تنظیم ترشولد
threshold_slider = ttk.Scale(root, from_=0, to=255, orient="horizontal", command=lambda value: update_threshold(int(float(value))))
threshold_slider.set(128)  # مقدار پیش‌فرض
threshold_slider.pack(pady=20)

# برچسب توضیحی برای اسلایدر
threshold_label_text = tk.Label(root, text="Adjust Threshold", font=("Helvetica", 12), fg="white", bg="#2C3E50")
threshold_label_text.pack()


# Variables for the images
original_image = None
grayscale_image = None
roi_coords = []

# Function to select and load an image
def select_image():
    global original_image, grayscale_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            original_image = Image.open(file_path)
            grayscale_image = ImageOps.grayscale(original_image)
            display_image(original_image, original_label)
        except Exception as e:
            print(f"Error loading image: {e}")

# Function to display an image in a label
def display_image(image, label):
    image.thumbnail((300, 300))  # Resize for display
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo

# Mouse event handlers for ROI selection
def start_roi_selection(event):
    global roi_coords
    roi_coords = [(event.x, event.y)]  # Start point
    print(f"Start ROI: {roi_coords[0]}")  # Debug

def end_roi_selection(event):
    global roi_coords
    if len(roi_coords) == 1:
        roi_coords.append((event.x, event.y))  # End point
        print(f"End ROI: {roi_coords[1]}")  # Debug
        show_roi()

# Function to extract and display the ROI
def show_roi():
    if original_image and len(roi_coords) == 2:
        x1, y1 = roi_coords[0]
        x2, y2 = roi_coords[1]
        x1, x2 = sorted([x1, x2])  # Ensure proper order
        y1, y2 = sorted([y1, y2])  # Ensure proper order
        
        # Scale coordinates to match the original image size
        scale_x = original_image.width / original_label.winfo_width()
        scale_y = original_image.height / original_label.winfo_height()
        x1, x2 = int(x1 * scale_x), int(x2 * scale_x)
        y1, y2 = int(y1 * scale_y), int(y2 * scale_y)
        
        print(f"Scaled ROI coordinates: ({x1}, {y1}) to ({x2}, {y2})")  # Debug
        
        # Crop the ROI
        roi_image = original_image.crop((x1, y1, x2, y2))
        
        # Show the ROI in a new window
        roi_window = tk.Toplevel(root)
        roi_window.title("Selected ROI")
        roi_window.geometry("300x300")
        roi_window.configure(bg="#2C3E50")
        
        roi_image.thumbnail((200, 200))  # Resize for display
        roi_photo = ImageTk.PhotoImage(roi_image)
        roi_label = tk.Label(roi_window, image=roi_photo, bg="#34495E")
        roi_label.image = roi_photo
        roi_label.pack(pady=20)

# Bind mouse events to the original image label
original_label.bind("<ButtonPress-1>", start_roi_selection)  # Start selection
original_label.bind("<ButtonRelease-1>", end_roi_selection)  # End selection

# Add a button to load the image
select_button = ttk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=10)

# Start the main application loop
root.mainloop()