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

        self.image_label = tk.Label(root, bg='black')  # Set background color to black
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # Resolution label setup
        self.resolution_label = tk.Label(root, text='', bg='black', fg='white', anchor='sw')
        self.resolution_label.pack(side=tk.BOTTOM, anchor='sw')

        # Set up key bindings
        self.root.bind('<Left>', self.show_previous_image)
        self.root.bind('<Right>', self.show_next_image)
        self.root.bind('<Escape>', self.handle_escape)

        # FullScreen Button
        self.full_screen_button = tk.Button(root, text="FullScreen", command=self.toggle_full_screen, bg='black', fg='white')
        self.full_screen_button.place(x=80, y=5)

        # Navigation Buttons
        self.prev_button = tk.Button(root, text="<---", command=self.show_previous_image, bg='black', fg='white')
        self.next_button = tk.Button(root, text="--->", command=self.show_next_image, bg='black', fg='white')
        self.prev_button.place(x=15, y=5)
        self.next_button.place(x=180, y=5)

        self.full_screen = False
        self.update_image()

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
            self.update_image()

    def update_image(self, scale_factor=1.0):
        if not self.image_list:
            return
        image = Image.open(self.image_list[self.current_index])
        if scale_factor != 1.0:
            width, height = image.size
            new_size = (int(width * scale_factor), int(height * scale_factor))
            image = image.resize(new_size, Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.tk_image)

        # Update the resolution label
        resolution_text = f"Resolution: {image.width} x {image.height}"
        self.resolution_label.config(text=resolution_text)

        self.root.title(f"{os.path.basename(self.image_list[self.current_index])}")

    def show_previous_image(self, event=None):
        if not self.image_list:
            return
        self.current_index = (self.current_index - 1) % len(self.image_list)
        self.update_image()
        if self.full_screen:
            self.zoom_to_fit()

    def show_next_image(self, event=None):
        if not self.image_list:
            return
        self.current_index = (self.current_index + 1) % len(self.image_list)
        self.update_image()
        if self.full_screen:
            self.zoom_to_fit()

    def handle_escape(self, event):
        if self.full_screen:
            self.toggle_full_screen()
        else:
            self.root.destroy()

    def toggle_full_screen(self, event=None):
        if not self.full_screen:
            self.root.attributes("-fullscreen", True)
            self.full_screen_button.place_forget()
            self.prev_button.place_forget()
            self.next_button.place_forget()
            self.resolution_label.pack_forget()  # Hide resolution label
            self.full_screen = True
            self.zoom_to_fit()
        else:
            self.root.attributes("-fullscreen", False)
            self.full_screen_button.place(x=80, y=5)
            self.prev_button.place(x=15, y=5)
            self.next_button.place(x=180, y=5)
            self.resolution_label.pack(side=tk.BOTTOM, anchor='sw')  # Show resolution label
            self.full_screen = False
            self.update_image()

    def zoom_to_fit(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        image = Image.open(self.image_list[self.current_index])
        width, height = image.size

        scale_width = screen_width / width
        scale_height = screen_height / height

        scale_factor = min(scale_width, scale_height)
        self.update_image(scale_factor)

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

    root = tk.Tk()
    viewer = ImageViewer(root, args.image)
    root.mainloop()

if __name__ == "__main__":
    main()
