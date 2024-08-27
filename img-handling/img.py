import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
from tkinterdnd2 import TkinterDnD, DND_FILES

class ImageCropper(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Cropper")
        self.geometry("800x600")

        self.image_path = None
        self.image = None
        self.crop_box = None
        self.drop_area = None

        self.canvas = tk.Canvas(self, bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.crop_button = ttk.Button(self.button_frame, text="Save Cropped Image", command=self.save_cropped_image)
        self.crop_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.canvas.bind("<ButtonPress-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.do_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)

        self.create_drop_area()

    def create_drop_area(self):
        self.drop_area = tk.Label(self.canvas, text="Drop Image Here", bg="lightgray", width=40, height=10)
        self.drop_area.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.drop_area.bind("<Button-1>", lambda e: self.open_file_dialog())
        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind("<<Drop>>", self.on_file_drop)

    def on_file_drop(self, event):
        self.image_path = event.data.strip("{}")
        self.load_image()

    def open_file_dialog(self):
        filetypes = (("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*"))
        self.image_path = filedialog.askopenfilename(title="Open Image", filetypes=filetypes)
        if self.image_path:
            self.load_image()

    def load_image(self):
        self.image = Image.open(self.image_path)
        self.image = ImageOps.exif_transpose(self.image)  # Correct image orientation
        self.display_image()

    def display_image(self):
        self.canvas.delete("all")  # Clear previous canvas content

        img_width, img_height = self.image.size
        ratio = min(self.canvas.winfo_width() / img_width, self.canvas.winfo_height() / img_height)
        resized_img = self.image.resize((int(img_width * ratio), int(img_height * ratio)), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(resized_img)
        self.canvas.create_image(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, anchor=tk.CENTER, image=self.tk_image)

        if self.drop_area:  # Remove the drop area label after loading the image
            self.drop_area.destroy()
            self.drop_area = None

    def start_crop(self, event):
        self.crop_box = [event.x, event.y]

    def do_crop(self, event):
        self.canvas.delete("crop_rect")
        x1, y1 = self.crop_box
        x2, y2 = event.x, event.y
        width = abs(x2 - x1)
        height = width * 2
        if y2 < y1:
            y2 = y1 - height
        else:
            y2 = y1 + height
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='red', tag="crop_rect")

    def end_crop(self, event):
        self.crop_box.extend([event.x, event.y])

    def save_cropped_image(self):
        if self.crop_box and self.image:
            x1, y1, x2, y2 = self.crop_box
            width = abs(x2 - x1)
            height = width * 2
            crop_area = (x1, y1, x1 + width, y1 + height)
            print(crop_area)
            cropped_image = self.image.crop(crop_area)
            resized_image = cropped_image.resize((600, 1200), Image.ANTIALIAS)
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
            if save_path:
                resized_image.save(save_path)
                self.quit()

if __name__ == "__main__":
    app = ImageCropper()
    app.mainloop()
