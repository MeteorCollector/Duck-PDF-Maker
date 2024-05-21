import os
from tkinter import Tk, Button, Label, Listbox, Scrollbar, filedialog
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ImageToPdfConverter:
    def __init__(self, master):
        self.master = master
        master.title("Image to PDF Converter")

        self.image_files = []

        self.label = Label(master, text="Select Image Files:")
        self.label.pack()

        self.listbox = Listbox(master, width=50, height=10, selectmode="extended")
        self.listbox.pack()

        self.scrollbar = Scrollbar(master, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.add_button = Button(master, text="Add Image", command=self.add_image)
        self.add_button.pack()

        self.convert_button = Button(master, text="Convert to PDF", command=self.convert_to_pdf)
        self.convert_button.pack()

    def add_image(self):
        file_paths = filedialog.askopenfilenames(title="Select Image Files", filetypes=[
                    ("image", ".jpg"),
                    ("image", ".jpeg"),
                    ("image", ".png"),
                    ("image", ".JPG"),
                    ("image", ".JPEG"),
                    ("image", ".PNG"),
                ])
        for file_path in file_paths:
            self.image_files.append(file_path)
            self.listbox.insert("end", os.path.basename(file_path))

    def convert_to_pdf(self):
        if not self.image_files:
            return

        output_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_pdf_path:
            return

        c = canvas.Canvas(output_pdf_path, pagesize=letter)
        width, height = letter
        for image_file in self.image_files:
            img = Image.open(image_file)
            img_width, img_height = img.size
            aspect_ratio = img_height / float(img_width)
            img_width = width
            img_height = int(width * aspect_ratio)
            c.setPageSize((img_width, img_height))
            c.drawImage(image_file, 0, 0, width=img_width, height=img_height)
            c.showPage()
        c.save()

        self.image_files.clear()
        self.listbox.delete(0, "end")
        print("PDF created successfully.")

if __name__ == "__main__":
    root = Tk()
    app = ImageToPdfConverter(root)
    root.mainloop()
