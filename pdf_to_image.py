import os
from tkinter import Label, Button, filedialog, Entry, IntVar
import fitz  # PyMuPDF

class PdfToImageConverter:
    def __init__(self, master, show_main_menu, texts):
       
        self.master = master
        self.show_main_menu = show_main_menu
        self.texts=texts

        self.pdf_path = None
        self.default_min_length = 1920

        self.frame = Label(master, text=texts["select_pdf"])
        self.frame.pack()

        self.choose_button = Button(master, text=texts["choose_pdf"], command=self.choose_pdf)
        self.choose_button.pack()

        # I realize that this doesn't change resolution of output

        # self.label_min_length = Label(master, text="Minimum length of the shortest side (px):")
        # self.label_min_length.pack()

        # self.min_length_var = IntVar(value=self.default_min_length)
        # self.entry_min_length = Entry(master, textvariable=self.min_length_var)
        # self.entry_min_length.pack()

        self.convert_button = Button(master, text=texts["convert_to_image"], command=self.convert_to_images)
        self.convert_button.pack()

        self.back_button = Button(master, text=texts["back_to_menu"], command=self.show_main_menu)
        self.back_button.pack()

        self.pdf_label = Label(master, text="")
        self.pdf_label.pack()

    def choose_pdf(self):
        self.pdf_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_path:
            self.pdf_label.config(text=os.path.basename(self.pdf_path))
        else:
            self.pdf_label.config(text="")

    def convert_to_images(self):
        if not self.pdf_path:
            return

        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return

        self.pdf_label.config(text=self.texts['processing'])
        # min_length = self.min_length_var.get()

        doc = fitz.open(self.pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            
            pdf_filename = os.path.splitext(os.path.basename(self.pdf_path))[0]
            output_file = os.path.join(output_dir, f"{pdf_filename}_page_{page_num + 1}.png")
            pix.save(output_file)
        doc.close()
        print("Images saved successfully.")
        self.pdf_label.config(text=self.texts['finished'])
    
    def update_texts(self, texts):
        self.texts = texts
        self.frame.config(text=self.texts['select_pdf'])
        self.choose_button.config(text=self.texts['choose_pdf'])
        self.convert_button.config(text=self.texts['convert_to_image'])
        self.back_button.config(text=self.texts['back_to_menu'])