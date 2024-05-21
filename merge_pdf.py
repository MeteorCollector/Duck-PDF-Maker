import os
from tkinter import Label, Button, Listbox, Scrollbar, filedialog, END
from PyPDF2 import PdfMerger

class MergePdfConverter:
    def __init__(self, master, show_main_menu, texts):
        self.master = master
        self.show_main_menu = show_main_menu

        self.pdf_files = []

        self.frame = Label(master, text=texts["select_pdfs_merge"])
        self.frame.pack()

        self.listbox = Listbox(master, width=50, height=10, selectmode="extended")
        self.listbox.pack()

        self.scrollbar = Scrollbar(master, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.choose_button = Button(master, text=texts["add_pdf_files"], command=self.add_pdfs)
        self.choose_button.pack()

        self.remove_button = Button(master, text=texts["remove_selected"], command=self.remove_selected)
        self.remove_button.pack()

        self.merge_button = Button(master, text=texts["merge_pdfs_button"], command=self.merge_pdfs)
        self.merge_button.pack()

        self.back_button = Button(master, text=texts["back_to_menu"], command=self.show_main_menu)
        self.back_button.pack()

    def add_pdfs(self):
        file_paths = filedialog.askopenfilenames(title="Select PDF Files", filetypes=[("PDF Files", "*.pdf")])
        for file_path in file_paths:
            if file_path not in self.pdf_files:
                self.pdf_files.append(file_path)
                self.listbox.insert(END, os.path.basename(file_path))

    def remove_selected(self):
        selected_indices = list(self.listbox.curselection())
        for index in selected_indices[::-1]:
            self.pdf_files.pop(index)
            self.listbox.delete(index)

    def merge_pdfs(self):
        if not self.pdf_files:
            return

        output_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_pdf_path:
            return

        pdf_merger = PdfMerger()
        for pdf_file in self.pdf_files:
            pdf_merger.append(pdf_file)

        with open(output_pdf_path, "wb") as out_file:
            pdf_merger.write(out_file)

        pdf_merger.close()
        self.pdf_files.clear()
        self.listbox.delete(0, END)
        print("PDFs merged successfully.")
    
    def update_texts(self, texts):
        self.texts = texts
        self.frame.config(text=self.texts['select_pdfs_merge'])
        self.choose_button.config(text=self.texts['add_pdf_files'])
        self.remove_button.config(text=self.texts['remove_selected'])
        self.merge_button.config(text=self.texts['merge_pdfs_button'])
        self.back_button.config(text=self.texts['back_to_menu'])
