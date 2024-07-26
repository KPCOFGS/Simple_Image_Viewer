import argparse
import os
import tkinter as tk
from PIL import Image, ImageTk
import glob

class ImageViewer:
    def __init__(self, root, image_path):
        self.root = root
        self.image_path = image_path
        self.image_list = self.get_image_list()
        self.current_index = self.image_list.index(image_path) if self.image_list else 0

        # Set the root window background color to black
        self.root.configure(bg='black')

        # Create top frame for buttons
        self.top_frame = tk.Frame(root, bg='black')
        self.top_frame.grid(row=0, column=0, sticky="ew")



        # Navigation Buttons
        self.prev_button = tk.Button(self.top_frame, text="<---", command=self.show_previous_image, bg='black', fg='white')
        self.prev_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.next_button = tk.Button(self.top_frame, text="--->", command=self.show_next_image, bg='black', fg='white')
        self.next_button.pack(side=tk.LEFT, padx=5, pady=5)
        # FullScreen Button
        self.full_screen_button = tk.Button(self.top_frame, text="FullScreen", command=self.toggle_full_screen, bg='black', fg='white')
        self.full_screen_button.pack(side=tk.LEFT, padx=5, pady=5)
        # Image display area
        self.image_label = tk.Label(root, bg='black')
        self.image_label.grid(row=1, column=0, sticky="nsew")

        # Resolution label setup
        self.resolution_label = tk.Label(root, text='', bg='black', fg='white', anchor='sw')
        self.resolution_label.grid(row=2, column=0, sticky="sw", padx=5, pady=5)

        # Configure row and column weights
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Set up key bindings
        self.root.bind('<Left>', self.show_previous_image)
        self.root.bind('<Right>', self.show_next_image)
        self.root.bind('<Escape>', self.handle_escape)

        self.full_screen = False

        # Initial image update to ensure correct scaling
        self.root.after(100, self.update_and_zoom_image)  # Slight delay to ensure GUI elements are fully initialized

        # Set window to maximized
        self.root.attributes('-zoomed', True)

        # Cursor visibility setup
        self.cursor_hidden = False
        self.root.bind('<Motion>', self.reset_cursor_timer)
        self.cursor_timer = None
        self.hide_cursor_delay = 2000  # 2 seconds

        # Periodically check for new images
        self.check_interval = 100  # Check every 5 seconds
        self.check_for_new_images()
        self.root.after(self.check_interval, self.update_image_periodically)
    def update_image_periodically(self):
        self.update_and_zoom_image()
        self.root.after(100, self.update_image_periodically)
    def get_image_list(self):
        directory = os.path.dirname(self.image_path)
        extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif']
        image_files = []
        for ext in extensions:
            image_files.extend(glob.glob(os.path.join(directory, ext)))
        image_files.sort(key=lambda x: os.path.splitext(x)[0].lower())
        return image_files

    def update_image_list(self):
        new_image_list = self.get_image_list()
        if new_image_list != self.image_list:
            self.image_list = new_image_list
            if not self.image_list:
                self.root.destroy()
                return
            self.current_index = min(self.current_index, len(self.image_list) - 1)
            self.update_and_zoom_image()

    def update_and_zoom_image(self, scale_factor=1.0):
        if not self.image_list:
            return

        image = Image.open(self.image_list[self.current_index])

        # Compute scale factor based on mode
        if self.full_screen:
            # Full screen mode
            max_width = self.root.winfo_width()
            max_height = self.root.winfo_height()
        else:
            # Fit to display area
            max_width = self.root.winfo_width()
            max_height = self.root.winfo_height() - self.top_frame.winfo_height() - self.resolution_label.winfo_height() - self.resolution_label.winfo_height()

        width, height = image.size

        # Avoid division by zero or negative values
        scale_width = max_width / (width) if width > 0 else 1.0
        scale_height = max_height / (height) if height > 0 else 1.0
        scale_factor = min(scale_width, scale_height)
        if scale_factor > 1.0 and self.full_screen == False:
            scale_factor = 1
        if scale_factor != 1.0 and scale_factor > 0:
            new_size = (int(width * scale_factor), int(height * scale_factor))
            if new_size[0] == 0:
                new_size = (1, new_size[1])
            if new_size[1] == 0:
                new_size = (new_size[0],1)
            image = image.resize(new_size, Image.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.tk_image)

        # Update the resolution label
        resolution_text = f"Resolution: {width}x{height}"
        self.resolution_label.config(text=resolution_text)

        self.root.title(f"{os.path.basename(self.image_list[self.current_index])}")

    def show_previous_image(self, event=None):
        if not self.image_list:
            return
        self.current_index = (self.current_index - 1) % len(self.image_list)
        self.update_and_zoom_image()

    def show_next_image(self, event=None):
        if not self.image_list:
            return
        self.current_index = (self.current_index + 1) % len(self.image_list)
        self.update_and_zoom_image()

    def handle_escape(self, event):
        if self.full_screen:
            self.toggle_full_screen()
        else:
            self.root.destroy()

    def toggle_full_screen(self, event=None):
        if not self.full_screen:
            self.root.attributes("-fullscreen", True)
            self.hide_top_buttons()
            self.full_screen = True
            self.root.after(100, self.update_and_zoom_image)
        else:
            self.root.attributes("-fullscreen", False)
            self.show_top_buttons()
            self.full_screen = False
            self.root.after(100, self.update_and_zoom_image)

    def hide_top_buttons(self):
        self.top_frame.grid_forget()  # Hide top frame
        self.resolution_label.grid_forget()  # Hide resolution label

    def show_top_buttons(self):
        self.top_frame.grid(row=0, column=0, sticky="ew")
        self.resolution_label.grid(row=2, column=0, sticky="sw", padx=5, pady=5)

    def reset_cursor_timer(self, event):
        if self.cursor_hidden:
            self.root.config(cursor="")
            self.cursor_hidden = False
        if self.cursor_timer:
            self.root.after_cancel(self.cursor_timer)
        self.cursor_timer = self.root.after(self.hide_cursor_delay, self.hide_cursor)

    def hide_cursor(self):
        if not self.cursor_hidden:
            self.root.config(cursor="none")
            self.cursor_hidden = True

    def check_for_new_images(self):
        self.update_image_list()
        self.root.after(self.check_interval, self.check_for_new_images)

def main():
    parser = argparse.ArgumentParser(description="Simple Image Viewer")
    parser.add_argument("image", help="Path to the image to start with")
    args = parser.parse_args()
    if not os.path.exists(args.image):
        print(f"Error: The path '{args.image}' does not exist.")
        return
    root = tk.Tk()
    viewer = ImageViewer(root, args.image)
    root.mainloop()

if __name__ == "__main__":
    main()
