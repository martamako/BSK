"""
This module provides functionality:
- Creating GUI app emulate electronic signature
"""
from tkinter import *
from tkinter.filedialog import askopenfilename
from Encrypting.Encrypting import *


class Page:
    def __init__(self, main_frame: Frame):
        self.key_path = None
        self.file_path = None
        self.main_frame = main_frame

    def document_page(self, lb_text: str):
        document_frame = Frame(self.main_frame)

        lb_document = Label(document_frame, text=lb_text)
        document_btn = Button(document_frame, text="Plik", font=("Bold", 12), fg="#158aff", bd=0, bg="#c3c3c3",
                              command=lambda: self.choose_file(lb_document))
        lb_document.pack(pady=10)
        document_btn.pack()
        document_frame.pack(pady=10)

    def key_page(self, key_text: str):
        key_frame = Frame(self.main_frame)
        lb_key = Label(key_frame, text=key_text)
        key_btn = Button(key_frame, text="Klucz", font=("Bold", 12), fg="#158aff", bd=0, bg="#c3c3c3",
                         command=lambda: self.choose_key(lb_key))

        lb_key.pack(pady=10)
        key_btn.pack()
        key_frame.pack(pady=10)

    def delete_pages(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

    def choose_file(self, label: Label):
        file_path = askopenfilename(
            title="Wybierz plik",
            filetypes=(
                ("Pliki tekstowe", "*.txt"), ("Pliki PDF", "*.pdf"), ("Pliki cpp", "*.cpp"), ("Wszystkie pliki", "*.*"))
        )
        if file_path:
            self.file_path = file_path
            print(f"Wybrany plik: {file_path}")
            label.config(text=f"Wybrany plik: {file_path}")

    def choose_key(self, label):
        file_path = askopenfilename(
            title="Wybierz plik",
            filetypes=(("Pliki tekstowe", "*.pem"), ("Wszystkie pliki", "*.*"))
        )
        if file_path:
            self.key_path = file_path
            print(f"Wybrany klucz: {file_path}")
            label.config(text=f"Wybrany klucz: {file_path}")


class SigningPage(Page):
    def __init__(self, main_frame: Frame):
        super().__init__(main_frame)
        self.entry = None
        self.signing_page()

    def signing_page(self):
        self.delete_pages()
        frame = Frame(self.main_frame)

        label = Label(frame, text="Wprowadź pin do odszyfrowania klucza")
        self.entry = Entry(frame, width=20)

        label.pack(padx=10, pady=10)
        self.entry.pack(padx=40, pady=10)

        self.document_page("Plik do podpisania")
        self.key_page("Zaszyfrowany klucz prywatny")

        button = Button(frame, text="Encrypting", font=("Bold", 12), fg="#158aff", bd=0,
                        bg="#c3c3c3", command=self.signing_file)
        button.pack(pady=10)
        frame.pack(pady=20)

    def signing_file(self):
        entered_text = self.entry.get()
        if entered_text == "":
            print("Brak pinu")
        elif check_pin(entered_text):
            sing_file(self.file_path, self.key_path, entered_text)
            print("Zaszyfrowano plik " + self.file_path)
        print(f'Wprowadzony tekst: {entered_text}')


class ValidationPage(Page):
    def __init__(self, main_frame: Frame):
        super().__init__(main_frame)
        self.validation_page()

    def validation_page(self):
        self.delete_pages()
        frame = Frame(self.main_frame)

        # lb = Label(validation_frame, text="Walidacja")
        button = Button(frame, text="Walidacja", font=("Bold", 12), fg="#158aff", bd=0,
                        bg="#c3c3c3", command=self.validation)

        self.document_page("Plik do weryfikacji")
        self.key_page("Klucz publiczny")
        # lb.pack(side=LEFT)
        button.pack(padx=20)
        frame.pack(pady=20)

    def validation(self):
        verify_file(self.file_path, "output.xml", self.key_path)


class EncryptingPage(Page):
    def __init__(self, main_frame: Frame):
        super().__init__(main_frame)
        self.encrypting_page()

    def encrypting_page(self):
        self.delete_pages()
        frame = Frame(self.main_frame)
        label = Label(frame, text="Encrypting pliku")
        label.pack(pady=10)

        self.document_page("Plik do zaszyfrowania")
        self.key_page("Klucz publiczny")

        encrypting_btn = Button(frame, text="Encrypting", font=("Bold", 12), fg="#158aff", bd=0,
                                bg="#c3c3c3", command=self.encrypting_file)
        encrypting_btn.pack(pady=10)

        frame.pack(pady=20)

    def encrypting_file(self):
        encrypt_file(self.file_path, self.key_path)


class DecryptingPage(Page):
    def __init__(self, main_frame: Frame):
        super().__init__(main_frame)
        self.decrypting_page()

    def decrypting_page(self):
        self.delete_pages()
        frame = Frame(self.main_frame)
        label = Label(frame, text="Deszyfrowanie pliku")
        label.pack(pady=10)

        self.document_page("Plik do odszyfrowania")
        self.key_page("Klucz prywatny")

        encrypting_btn = Button(frame, text="Odszyfrowanie", font=("Bold", 12), fg="#158aff", bd=0,
                                bg="#c3c3c3", command=self.decrypting_file)
        encrypting_btn.pack(pady=10)

        frame.pack(pady=20)

    def decrypting_file(self):
        decrypt_file(self.file_path, self.key_path)


class App:
    def __init__(self):
        self.window = None
        self.main_frame = None
        self.options_frame = None

        self.signing_p = None
        self.signing_btn = None

        self.validation_p = None
        self.validation_btn = None

        self.encrypting_p = None
        self.encrypting_btn = None

        self.decrypting_p = None
        self.decrypting_btn = None

        self.create_window()

    def create_window(self):
        self.window = Tk()
        self.window.geometry("600x500+300+100")
        self.window.title("Projekt BSK")

        self.create_menu()
        self.create_main_frame()

        self.window.mainloop()

    def create_menu(self):
        self.options_frame = Frame(self.window, bg="#c3c3c3")
        self.options_frame.pack(side=LEFT)
        self.options_frame.propagate(False)
        self.options_frame.configure(width=200, height=500)

        self.signing_btn = Button(self.options_frame, text="Podpisywanie", font=("Bold", 15), fg="#158aff", bd=0,
                                  bg="#c3c3c3", command=self.signing_page)
        self.signing_btn.place(x=10, y=100)

        self.validation_btn = Button(self.options_frame, text="Walidacja", font=("Bold", 15), fg="#158aff", bd=0,
                                     bg="#c3c3c3", command=self.validation_page)
        self.validation_btn.place(x=10, y=150)

        self.encrypting_btn = Button(self.options_frame, text="Encrypting", font=("Bold", 15), fg="#158aff", bd=0,
                                     bg="#c3c3c3", command=self.encrypting_page)
        self.encrypting_btn.place(x=10, y=200)

        self.decrypting_btn = Button(self.options_frame, text="Deszyfrowanie", font=("Bold", 15), fg="#158aff", bd=0,
                                     bg="#c3c3c3", command=self.decrypting_page)
        self.decrypting_btn.place(x=10, y=250)

    def create_main_frame(self):
        self.main_frame = Frame(self.window, highlightbackground='black', highlightthickness=2)
        self.main_frame.pack(side=LEFT)
        self.main_frame.propagate(False)
        self.main_frame.configure(height=500, width=600)

    def signing_page(self):
        self.signing_p = SigningPage(self.main_frame)

    def validation_page(self):
        self.validation_p = ValidationPage(self.main_frame)

    def encrypting_page(self):
        self.encrypting_p = EncryptingPage(self.main_frame)

    def decrypting_page(self):
        self.decrypting_p = DecryptingPage(self.main_frame)


if __name__ == "__main__":
    app = App()