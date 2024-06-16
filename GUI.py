from tkinter import *
from tkinter.filedialog import askopenfilename

from Szyfrowanie.Szyfrowanie import *


class Application:
    def __init__(self):
        self.file_path = None
        self.key_path = None
        self.entry = None
        self.options_frame = None
        self.encrypting_btn = None
        self.validation_btn = None
        self.signing_btn = None
        self.window = None
        self.main_frame = None
        self.create_window()

    def create_window(self):
        self.window = Tk()
        self.window.geometry("600x500+300+100")
        self.window.title("Projekt BSK")

        self.create_menu()
        self.create_pages()

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

        self.encrypting_btn = Button(self.options_frame, text="(De)Szyfrowanie", font=("Bold", 15), fg="#158aff", bd=0,
                                     bg="#c3c3c3", command=self.encrypting_page)
        self.encrypting_btn.place(x=10, y=200)

    def create_pages(self):
        self.main_frame = Frame(self.window, highlightbackground='black', highlightthickness=2)
        self.main_frame.pack(side=LEFT)
        self.main_frame.propagate(False)
        self.main_frame.configure(height=500, width=600)

    def signing_page(self):
        self.delete_pages()
        signing_frame = Frame(self.main_frame)

        lb_szyfrowanie = Label(signing_frame, text="Wprowadź pin do odszyfrowania klucza")
        self.entry = Entry(signing_frame, width=20)

        lb_szyfrowanie.pack(padx=10, pady=10)
        self.entry.pack(padx=40, pady=10)

        self.document_page("Plik do podpisania")
        self.key_page("Zaszyfrowany klucz prywatny")

        encrypting_btn = Button(signing_frame, text="Szyfrowanie", font=("Bold", 12), fg="#158aff", bd=0,
                                bg="#c3c3c3", command=self.encrypting_file)
        encrypting_btn.pack(pady=10)
        signing_frame.pack(pady=20)

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

    def validation_page(self):
        self.delete_pages()
        validation_frame = Frame(self.main_frame)

        # lb = Label(validation_frame, text="Walidacja")
        validation_btn = Button(validation_frame, text="Walidacja", font=("Bold", 12), fg="#158aff", bd=0,
                                bg="#c3c3c3", command=self.validation)

        self.document_page("Plik do weryfikacji")
        self.key_page("Klucz publiczny")
        # lb.pack(side=LEFT)
        validation_btn.pack(padx=20)
        validation_frame.pack(pady=20)

    def encrypting_page(self):
        self.delete_pages()
        encrypting_page = Frame(self.main_frame)

        encrypting_btn = Button(encrypting_page, text="Szyfrowanie", font=("Bold", 12), fg="#158aff", bd=0,
                                bg="#c3c3c3", command=self.encrypting_file)
        encrypting_btn.pack(pady=10)
        encrypting_page.pack(pady=20)

    def delete_pages(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

    def choose_file(self, label):
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

    def encrypting_file(self):
        entered_text = self.entry.get()
        if entered_text == "":
            print("Brak pinu")
        elif check_pin(entered_text):
            sing_file(self.file_path, self.key_path, entered_text)
            print("Zaszyfrowano plik " + self.file_path)
        print(f'Wprowadzony tekst: {entered_text}')

    def validation(self):
        verify_file(self.file_path, "output.xml", self.key_path)


if __name__ == "__main__":
    app = Application()
