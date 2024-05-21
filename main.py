from tkinter import Tk, Frame, Button, Label, StringVar, OptionMenu
from image_to_pdf import ImageToPdfConverter
from pdf_to_image import PdfToImageConverter
from split_pdf import SplitPdfConverter
from merge_pdf import MergePdfConverter
from lang import LANGUAGES

class App:
    def __init__(self, master):
        self.master = master
        self.current_lang = 'en'
        self.texts = LANGUAGES[self.current_lang]
        
        master.title(self.texts['title'])

        self.main_menu = Frame(master)
        self.image_to_pdf_frame = Frame(master)
        self.pdf_to_image_frame = Frame(master)
        self.split_pdf_frame = Frame(master)
        self.merge_pdf_frame = Frame(master)

        self.lang_var = StringVar(master)
        self.lang_var.set(self.current_lang)
        self.lang_menu = OptionMenu(master, self.lang_var, *LANGUAGES.keys(), command=self.change_language)
        self.lang_menu.pack()

        self.create_main_menu()
        self.image_to_pdf_converter = ImageToPdfConverter(self.image_to_pdf_frame, self.show_main_menu, self.texts)
        self.pdf_to_image_converter = PdfToImageConverter(self.pdf_to_image_frame, self.show_main_menu, self.texts)
        self.split_pdf_converter = SplitPdfConverter(self.split_pdf_frame, self.show_main_menu, self.texts)
        self.merge_pdf_converter = MergePdfConverter(self.merge_pdf_frame, self.show_main_menu, self.texts)

        self.show_frame(self.main_menu)

    def create_main_menu(self):
        for widget in self.main_menu.winfo_children():
            widget.destroy()

        Label(self.main_menu, text=self.texts['select_option']).pack()
        Button(self.main_menu, text=self.texts['image_to_pdf'], command=lambda: self.show_frame(self.image_to_pdf_frame)).pack()
        Button(self.main_menu, text=self.texts['pdf_to_image'], command=lambda: self.show_frame(self.pdf_to_image_frame)).pack()
        Button(self.main_menu, text=self.texts['split_pdf'], command=lambda: self.show_frame(self.split_pdf_frame)).pack()
        Button(self.main_menu, text=self.texts['merge_pdfs'], command=lambda: self.show_frame(self.merge_pdf_frame)).pack()
        Label(self.main_menu, text=self.texts['description']).pack()

    def show_frame(self, frame):
        self.main_menu.pack_forget()
        self.image_to_pdf_frame.pack_forget()
        self.pdf_to_image_frame.pack_forget()
        self.split_pdf_frame.pack_forget()
        self.merge_pdf_frame.pack_forget()
        frame.pack()

    def show_main_menu(self):
        self.show_frame(self.main_menu)

    def change_language(self, lang):
        self.current_lang = lang
        self.texts = LANGUAGES[self.current_lang]
        self.master.title(self.texts['title'])
        self.create_main_menu()
        self.image_to_pdf_converter.update_texts(self.texts)
        self.pdf_to_image_converter.update_texts(self.texts)
        self.split_pdf_converter.update_texts(self.texts)
        self.merge_pdf_converter.update_texts(self.texts)

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.geometry("600x400")
    root.mainloop()
