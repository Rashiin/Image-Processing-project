

Image Processing Toolkit with Grayscale, Negative, Threshold, and ROI Selection 🎨
An interactive image processing application built with Python's tkinter GUI toolkit. This tool provides various image transformations and allows users to select regions of interest (ROI) for further analysis.

Features
Image Selection: Load images in formats such as .jpg, .jpeg, .png, .bmp, and .gif.
Grayscale Conversion: Convert the loaded image to grayscale and display it.
Negative and Thresholding:
View the negative (inverted) version of the grayscale image.
Apply an adjustable threshold to create a binary image.
Histogram Visualization:
Display the original histogram of the grayscale image.
Display the equalized histogram to enhance contrast.
Region of Interest (ROI):
Select a specific area of the image with mouse clicks.
Display the selected ROI in a pop-up window.
Dependencies
Make sure the following Python libraries are installed:

bash
Copy code
pip install tkinter pillow matplotlib numpy
How to Use
Clone the repository:
bash
Copy code
git clone https://github.com/Rashiin/image-processing.git
Navigate to the project folder:
bash
Copy code
cd your-repository
Run the script:
bash
Copy code
python image_processing_toolkit.py
Instructions
Select Image:
Click the "Select Image" button to load an image from your computer.
View Grayscale, Negative, and Thresholded Images:
Grayscale, negative, and thresholded versions of the image will be displayed in real time.
Use the slider to adjust the threshold value.
Show Histograms:
Click "Show Original Histogram" to view the pixel intensity distribution.
Click "Show Equalized Histogram" to view the contrast-enhanced histogram.
Region of Interest (ROI) Selection:
Click and drag on the original image to select a rectangular region.
Release the mouse to display the selected ROI.
Screenshots
1. Main Window
Displays the original, grayscale, negative, and threshold images side by side.

2. Histogram
Shows the histogram for the grayscale image.

3. ROI Selection
A pop-up window displays the selected region of interest.

File Structure
plaintext
Copy code
│── image_processing_toolkit.py  # Main application script
├── README.md                    # Project documentation
└── screenshots/                  # (Optional) Store screenshots for demonstration
Future Improvements
Support for more image filters (e.g., blur, sharpen).
Ability to save processed images.
Add custom color mapping options.
Contributing
Pull requests are welcome. For major changes, please open an issue to discuss what you would like to change.



