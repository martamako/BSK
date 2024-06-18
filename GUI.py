"""
This module provides functionality:
- Creating GUI app emulate electronic signature
"""
from tkinter import *
from tkinter.filedialog import askopenfilename
from Encrypting.Encrypting import *


class Page:
    """
    Class Page is base class for creating pages with different functionalities.
    """
    def __init__(self, main_frame: Frame):
        """
        Constructor taking main frame of application's window.
        :param main_frame: Frame created from application's window. It's frame on which all other frames will be placed.
        """
        self.key_path = None
        self.file_path = None
        self.main_frame = main_frame

    def page(self, text: str, document_page_str: str, key_page_str: str):
        """
        Creating page with text for button, document_page_str for label in document frame
        and key_page_str for label in key frame.
        :param text: Text that will be on button.
        :param document_page_str: Text displayed on label before button to choose file
        :param key_page_str: Text displayed on label before button to choose file with key
        :return:
        """
        self.delete_pages()
        frame = Frame(self.main_frame)

        button = Button(frame, text=text, font=("Bold", 12), fg="#158aff", bd=0,
                        bg="#c3c3c3", command=self.functionality)

        self.document_page(document_page_str)
        self.key_page(key_page_str)

        button.pack(padx=20)
        frame.pack(pady=20)

    def functionality(self):
        """
        In base class it's abstract method. Implementation in subclasses.
        :return:
        """
        pass

    def document_page(self, lb_text: str):
        """
        Method to create frame with elements to choose file for functionality.
        :param lb_text: Text that will be displayed on label before button to choose file
        :return:
        """
        document_frame = Frame(self.main_frame)

        lb_document = Label(document_frame, text=lb_text)
        document_btn = Button(document_frame, text="Plik", font=("Bold", 12), fg="#158aff", bd=0, bg="#c3c3c3",
                              command=lambda: self.choose_file(lb_document))
        lb_document.pack(pady=10)
        document_btn.pack()
        document_frame.pack(pady=10)

    def key_page(self, key_text: str):
        """
        Method to create frame with elements to choose file with key.
        :param key_text: Text that will be displayed on label before button to choose file with key
        :return:
        """
        key_frame = Frame(self.main_frame)
        lb_key = Label(key_frame, text=key_text)
        key_btn = Button(key_frame, text="Klucz", font=("Bold", 12), fg="#158aff", bd=0, bg="#c3c3c3",
                         command=lambda: self.choose_key(lb_key))

        lb_key.pack(pady=10)
        key_btn.pack()
        key_frame.pack(pady=10)

    def delete_pages(self):
        """
        Deletes pages from main frame to leave it empty for new page
        :return:
        """
        for frame in self.main_frame.winfo_children():
            frame.destroy()

    def choose_file(self, label: Label):
        """
        Function to choose file for functionality and changing text of label to include chosen file.
        Sets file_path to path of chosen file for further processing in functionality.
        :param label: Label to put text after choosing file
        :return:
        """
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
        """
        Function to choose file with key and changing text of label to include chosen key.
        Sets key_path to path of chosen key for further processing in functionality.
        :param label: Label to put text after choosing key
        :return:
        """
        file_path = askopenfilename(
            title="Wybierz plik",
            filetypes=(("Pliki tekstowe", "*.pem"), ("Wszystkie pliki", "*.*"))
        )
        if file_path:
            self.key_path = file_path
            print(f"Wybrany klucz: {file_path}")
            label.config(text=f"Wybrany klucz: {file_path}")


class SigningPage(Page):
    """
    Subclass of class Page. This class is meant to create page for signing functionality.
    """
    def __init__(self, main_frame: Frame):
        super().__init__(main_frame)
        self.entry = None
        self.page()

    def page(self, text="Podpisanie", document_page_str="Plik do podpisania", key_page_str="Zaszyfrowany klucz prywatny"):
        """
        Implementation of method page. Parameters are set to text for signing page functionality.
        To parent class it also adds enetering PIN to decrypt private key.
        :param text: Text that will be on button.
        :param document_page_str: Text displayed on label before button to choose file
        :param key_page_str: Text displayed on label before button to choose file with key
        :return:
        """
        self.delete_pages()
        frame = Frame(self.main_frame)

        self.document_page(document_page_str)
        self.key_page(key_page_str)
        self.pin_page("Wprowadź pin do odszyfrowania klucza")

        button = Button(frame, text=text, font=("Bold", 12), fg="#158aff", bd=0,
                        bg="#c3c3c3", command=self.functionality)
        button.pack(pady=10)
        frame.pack(pady=20)

    def pin_page(self, text: str):
        """
        Creating page for entering PIN. Takes parameter text to set it to label.
        :param text: Set text to label.
        :return:
        """
        pin_frame = Frame(self.main_frame)

        label = Label(pin_frame, text=text)
        self.entry = Entry(pin_frame, width=20)

        label.pack(padx=10, pady=10)
        self.entry.pack(padx=40, pady=10)
        pin_frame.pack(pady=10)

    def functionality(self):
        """
        Provides signing functionality from Encrypting module.
        :return:
        """
        entered_text = self.entry.get()
        if entered_text == "":
            print("Brak pinu")
        elif check_pin(entered_text):
            sing_file(self.file_path, self.key_path, entered_text)
            print("Zaszyfrowano plik " + self.file_path)
        print(f'Wprowadzony tekst: {entered_text}')


class ValidationPage(Page):
    """
    Subclass of class Page. This class is meant to create page for validation functionality.
    """
    def __init__(self, main_frame: Frame):
        super().__init__(main_frame)
        # self.page()

    def page(self, text="Walidacja", document_page_str="Plik do weryfikacji", key_page_str="Klucz publiczny"):
        super().page(text, document_page_str, key_page_str)

    def functionality(self):
        """
        Validates chosen file with signature with 'output.xml' with chosen key.
        :return:
        """
        verify_file(self.file_path, "output.xml", self.key_path)


class EncryptingPage(Page):
    """
    Subclass of class Page. This class is meant to create page for encrypting functionality.
    """
    def __init__(self, main_frame: Frame):
        super().__init__(main_frame)

    def page(self, text="Szyfrowanie", document_page_str="Plik do zaszyfrowania", key_page_str="Klucz publiczny"):
        super().page(text, document_page_str, key_page_str)

    def functionality(self):
        """
        Encrypts chosen file with chosen key.
        :return:
        """
        encrypt_file(self.file_path, self.key_path)


class DecryptingPage(Page):
    """
    Subclass of class Page. This class is meant to create page for decrypting functionality.
    """
    def __init__(self, main_frame: Frame):
        super().__init__(main_frame)

    def page(self, text="Odszyfrowanie", document_page_str="Plik do odszyfrowania", key_page_str="Klucz prywatny"):
        super().page(text, document_page_str, key_page_str)

    def functionality(self):
        """
        Decrypts chosen file with chosen key.
        :return:
        """
        decrypt_file(self.file_path, self.key_path)


class App:
    """
    Class responsible for creating GUI app
    """
    def __init__(self):
        """
        Creates window and all necessary elements to display app
        """
        self.window = Tk()
        self.main_frame = Frame(self.window, highlightbackground='black', highlightthickness=2)
        self.options_frame = Frame(self.window, bg="#c3c3c3")

        self.signing_page = SigningPage(self.main_frame)
        self.signing_btn = None

        self.validation_page = ValidationPage(self.main_frame)
        self.validation_btn = None

        self.encrypting_page = EncryptingPage(self.main_frame)
        self.encrypting_btn = None

        self.decrypting_page = DecryptingPage(self.main_frame)
        self.decrypting_btn = None

        self.create_window()

    def create_window(self):
        """
        Creates window, calls methods to create menu and main frame.
        :return:
        """
        self.window.geometry("600x500+300+100")
        self.window.title("Projekt BSK")

        self.create_menu()
        self.create_main_frame()

        self.window.mainloop()

    def create_main_frame(self):
        """
        Creates main frame and sets design.
        :return:
        """
        self.main_frame.pack(side=LEFT)
        self.main_frame.propagate(False)
        self.main_frame.configure(height=500, width=600)

    def create_menu(self):
        """
        Creates menu and buttons each for different page.
        :return:
        """
        self.options_frame.pack(side=LEFT)
        self.options_frame.propagate(False)
        self.options_frame.configure(width=200, height=500)

        self.signing_btn = Button(self.options_frame, text="Podpisywanie", font=("Bold", 15), fg="#158aff", bd=0,
                                  bg="#c3c3c3", command=self.signing_page.page)
        self.signing_btn.place(x=10, y=100)

        self.validation_btn = Button(self.options_frame, text="Walidacja", font=("Bold", 15), fg="#158aff", bd=0,
                                     bg="#c3c3c3", command=self.validation_page.page)
        self.validation_btn.place(x=10, y=150)

        self.encrypting_btn = Button(self.options_frame, text="Szyfrowanie", font=("Bold", 15), fg="#158aff", bd=0,
                                     bg="#c3c3c3", command=self.encrypting_page.page)
        self.encrypting_btn.place(x=10, y=200)

        self.decrypting_btn = Button(self.options_frame, text="Deszyfrowanie", font=("Bold", 15), fg="#158aff", bd=0,
                                     bg="#c3c3c3", command=self.decrypting_page.page)
        self.decrypting_btn.place(x=10, y=250)


if __name__ == "__main__":
    app = App()
