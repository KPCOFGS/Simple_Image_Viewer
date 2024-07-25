# Simple Image Viewer

A basic image viewer application built with Python's Tkinter and PIL (Pillow) libraries. This application allows you to view images in a directory, navigate through them using buttons or arrow keys, and toggle fullscreen mode. It also hides the cursor when it's inactive after 2 seconds.

## Features
* View Images: Displays images in a given directory.
* Navigation: Navigate through images using left and right buttons or arrow keys.
* Fullscreen Mode: Toggle fullscreen mode with a button.
* Cursor Hiding: The cursor will disappear after 2 seconds of inactivity.
* Dynamic Image List: Automatically updates the image list if new images are added to the directory.
## Requirements
* Python 3.x
* Pillow library (pip install pillow)
## Installation

**Clone the repository:**
```bash
git clone 
cd image-viewer
```
**Install the required Python libraries:**
```bash
pip install pillow
```
## Usage

1. **Run the script with the path to the starting image:**
```bash
python image_viewer.py /path/to/your/image.jpg
```
2. **Navigation Controls:**
* Left Arrow: View the previous image.
* Right Arrow: View the next image.
* <---: View the previous image (Button).
* --->: View the next image (Button).
* Esc: Exit fullscreen mode or close the application.
3. **Fullscreen Mode:**
* Click the FullScreen button to toggle fullscreen mode.
* Press Esc to exit fullscreen mode.
## Script Details
* Image List: The application collects all images in the directory of the starting image (supports .png, .jpg, .jpeg, .gif formats).
* Image Scaling: When toggling fullscreen, the image is resized to fit the screen while maintaining its aspect ratio.
* Cursor Handling: The cursor will disappear after 2 seconds of inactivity and reappear with movement.
## Troubleshooting
* No Images Displayed: Ensure the path provided contains image files and that they have supported formats.
* Script Errors: Ensure you have the necessary permissions to access the images and run the script.
## Contributing
* Feel free to fork the repository and submit pull requests. For feature requests or bug reports, please open an issue.

## License
This project is licensed under the Unlicense. See the [LICENSE](LICENSE) file for details.

