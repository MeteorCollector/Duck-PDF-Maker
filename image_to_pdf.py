import os
from tkinter import Label, Listbox, Scrollbar, Button, filedialog
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ImageToPdfConverter:
    def __init__(self, master, show_main_menu, texts):
        self.master = master
        self.show_main_menu = show_main_menu
        self.texts=texts

        self.image_files = []

        self.frame = Label(master, text=self.texts['select_images'])
        self.frame.pack()

        self.listbox = Listbox(master, width=50, height=10, selectmode="extended")
        self.listbox.pack()

        self.scrollbar = Scrollbar(master, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.add_button = Button(master, text=self.texts['add_image'], command=self.add_image)
        self.add_button.pack()

        self.remove_button = Button(master, text=self.texts['remove_selected'], command=self.remove_selected)
        self.remove_button.pack()

        self.convert_button = Button(master, text=self.texts['convert_to_pdf'], command=self.convert_to_pdf)
        self.convert_button.pack()

        self.back_button = Button(master, text=self.texts['back_to_menu'], command=self.show_main_menu)
        self.back_button.pack()

    def add_image(self):
        file_paths = filedialog.askopenfilenames(title="Select Image Files", filetypes=[
                    ("image", ".jpg"),
                    ("image", ".jpeg"),
                    ("image", ".png"),
                    ("image", ".JPG"),
                    ("image", ".JPEG"),
                    ("image", ".PNG"),
                    ("image", ".gif"),
                    ("image", ".tiff"),
                    ("image", ".bmp"),
                ])
        for file_path in file_paths:
            if file_path not in self.image_files:
                self.image_files.append(file_path)
                self.listbox.insert("end", os.path.basename(file_path))

    def remove_selected(self):
        selected_indices = list(self.listbox.curselection())
        for index in selected_indices[::-1]:
            self.image_files.pop(index)
            self.listbox.delete(index)

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

    
    def update_texts(self, texts):
        self.texts = texts
        self.frame.config(text=self.texts['select_images'])
        self.add_button.config(text=self.texts['add_image'])
        self.remove_button.config(text=self.texts['remove_selected'])
        self.convert_button.config(text=self.texts['convert_to_pdf'])
        self.back_button.config(text=self.texts['back_to_menu'])
