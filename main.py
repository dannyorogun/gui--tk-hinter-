import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarker")
        self.root.geometry("600x500")
        self.image = None

        self.create_widgets()

    def create_widgets(self):
        # Upload Button
        self.upload_btn = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=10)

        # Canvas for displaying the image
        self.canvas = tk.Canvas(self.root, width=500, height=300, bg='lightgrey')
        self.canvas.pack(pady=10)

        # Watermark Entry
        self.watermark_text = tk.Entry(self.root, width=40)
        self.watermark_text.insert(0, "YourWebsite.com")
        self.watermark_text.pack(pady=5)

        # Add Watermark Button
        self.add_btn = tk.Button(self.root, text="Add Watermark", command=self.add_watermark)
        self.add_btn.pack(pady=10)

        # Save Button
        self.save_btn = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_btn.pack(pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.image_path = file_path
        self.image = Image.open(file_path).convert("RGBA")
        self.display_image(self.image)

    def display_image(self, img):
        # Resize for display
        img.thumbnail((500, 300))
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(250, 150, image=self.tk_img)

    def add_watermark(self):
        if not self.image:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        text = self.watermark_text.get()
        if not text:
            messagebox.showerror("Error", "Please enter watermark text.")
            return

        # Copy image to avoid altering original
        watermarked = self.image.copy()
        width, height = watermarked.size

        draw = ImageDraw.Draw(watermarked)

        # Use a default font; customize path or font if needed
        font = ImageFont.truetype("arial.ttf", int(height / 20))

        # Position: bottom-right
        text_width, text_height = draw.textsize(text, font)
        position = (width - text_width - 10, height - text_height - 10)

        # Add text to image
        draw.text(position, text, font=font, fill=(255, 255, 255, 128))

        self.image = watermarked
        self.display_image(self.image)

    def save_image(self):
        if not self.image:
            messagebox.showerror("Error", "No image to save.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
        if save_path:
            # Convert to RGB before saving if needed
            if self.image.mode == "RGBA":
                self.image = self.image.convert("RGB")
            self.image.save(save_path)
            messagebox.showinfo("Saved", f"Image saved at:\n{save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()



