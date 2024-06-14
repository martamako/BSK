from tkinter import *
from tkinter.filedialog import askopenfilename

from Szyfrowanie.Szyfrowanie import Szyfrowanie

class Application:
    def __init__(self):
        self.szyfrowanie = Szyfrowanie()
        self.create_window()


    def create_window(self):
        self.window = Tk()
        self.window.geometry("500x400+300+100")
        self.window.title("Projekt BSK")

        self.create_menu()
        self.create_pages()

        self.window.mainloop()

    def create_menu(self):
        self.options_frame = Frame(self.window, bg="#c3c3c3")
        self.options_frame.pack(side=LEFT)
        self.options_frame.propagate(False)
        self.options_frame.configure(width=150, height=400)

        self.encrypting_btn = Button(self.options_frame, text="Szyfrowanie", font=("Bold", 15), fg="#158aff", bd=0,
                                     bg="#c3c3c3",
                                     command=self.szyfrowanie_page)
        self.encrypting_btn.place(x=10, y=100)

        self.decrypting_btn = Button(self.options_frame, text="Walidacja", font=("Bold", 15), fg="#158aff", bd=0,
                                     bg="#c3c3c3",
                                     command=self.walidacja_page)
        self.decrypting_btn.place(x=10, y=150)

    def create_pages(self):
        self.main_frame = Frame(self.window, highlightbackground='black', highlightthickness=2)
        self.main_frame.pack(side=LEFT)
        self.main_frame.propagate(False)
        self.main_frame.configure(height=400, width=500)


    def szyfrowanie_page(self):
        self.delete_pages()
        szyfrowanie_frame = Frame(self.main_frame)

        lb_szyfrowanie = Label(szyfrowanie_frame, text="Wprowadź pin do odszyfrowania klucza")
        self.entry = Entry(szyfrowanie_frame, width=20)

        lb_szyfrowanie.pack(padx=10, pady=10)
        self.entry.pack(padx=40, pady=10)


        self.document_page()
        self.key_page()

        encrypting_btn = Button(szyfrowanie_frame, text="Szyfrowanie", font=("Bold", 12), fg="#158aff", bd=0,
                                bg="#c3c3c3",
                                command=self.szyfrowanie_file)
        encrypting_btn.pack(pady=10)
        szyfrowanie_frame.pack(pady=20)

    def document_page(self):
        document_frame = Frame(self.main_frame)

        lb_document = Label(document_frame, text="Plik do zaszyfrowania")
        document_btn = Button(document_frame, text="Plik", font=("Bold", 12), fg="#158aff", bd=0, bg="#c3c3c3",
                              command=lambda: self.choose_file(lb_document))
        lb_document.pack(pady=10)
        document_btn.pack()
        document_frame.pack(pady=10)

    def key_page(self):
        klucz_frame = Frame(self.main_frame)
        lb_klucz = Label(klucz_frame, text="Zaszyfrowany klucz prywatny")
        klucz_btn = Button(klucz_frame, text="Klucz", font=("Bold", 12), fg="#158aff", bd=0, bg="#c3c3c3",
                           command=lambda: self.choose_key(lb_klucz))

        lb_klucz.pack(pady=10)
        klucz_btn.pack()
        klucz_frame.pack(pady=10)

    def walidacja_page(self):
        self.delete_pages()
        walidacja_frame = Frame(self.main_frame)

        lb = Label(walidacja_frame, text="Walidacja")
        decrypting_btn = Button(walidacja_frame, text="Walidacja", font=("Bold", 12), fg="#158aff", bd=0,
                                bg="#c3c3c3",
                                command=self.walidacja)

        lb.pack(side=LEFT)
        decrypting_btn.pack(padx=20)
        walidacja_frame.pack(pady=20)

    def delete_pages(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

    def choose_file(self, label):
        file_path = askopenfilename(
            title="Wybierz plik",
            filetypes=(("Pliki tekstowe", "*.txt"), ("Pliki PDF", "*.pdf"), ("Pliki cpp", "*.cpp"), ("Wszystkie pliki", "*.*"))
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

    def szyfrowanie_file(self):
        entered_text = self.entry.get()
        if entered_text == "":
            print("Brak pinu")
        elif self.szyfrowanie.check_pin(entered_text):
            self.szyfrowanie.sing_file(self.file_path, self.key_path)
            print("Zaszyfrowano plik " + self.file_path)
        print(f'Wprowadzony tekst: {entered_text}')

    def walidacja(self):
        filename = askopenfilename()
        self.szyfrowanie.verify_file(filename)


if __name__ == "__main__":
    app = Application()