import os
from tkinter import Label, Button, filedialog
from PyPDF2 import PdfReader, PdfWriter

class SplitPdfConverter:
    def __init__(self, master, show_main_menu, texts):
        self.master = master
        self.show_main_menu = show_main_menu

        self.pdf_path = None

        self.frame = Label(master, text=texts["select_pdf_split"])
        self.frame.pack()

        self.choose_button = Button(master, text=texts["choose_pdf"], command=self.choose_pdf)
        self.choose_button.pack()

        self.split_button = Button(master, text=texts["split_pdf_button"], command=self.split_pdf)
        self.split_button.pack()

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

    def split_pdf(self):
        if not self.pdf_path:
            return

        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return

        pdf_reader = PdfReader(self.pdf_path)
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])

            output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(self.pdf_path))[0]}_page_{page_num + 1}.pdf")
            with open(output_file, "wb") as out_file:
                pdf_writer.write(out_file)

        print("PDF split successfully.")
    
    def update_texts(self, texts):
        self.texts = texts
        self.frame.config(text=self.texts['select_pdf_split'])
        self.choose_button.config(text=self.texts['choose_pdf'])
        self.split_button.config(text=self.texts['split_pdf_button'])
        self.back_button.config(text=self.texts['back_to_menu'])

