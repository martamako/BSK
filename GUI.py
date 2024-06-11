from tkinter import *
import tkinter.ttk as ttk

class Application:
    def __init__(self):
        self.window = Tk()

        self.cb_value = StringVar()
        self.label_value = StringVar()
        self.label_value.set("Szyfrowanie")

        self.combobox = ttk.Combobox(self.window, textvariable= self.cb_value)
        self.combobox.place(x = 50, y = 100)
        self.combobox['values'] = ("Szyfrowanie", "Deszyfrowanie")
        self.combobox.current(0)
        self.combobox.bind("<<ComboboxSelected>>", self.on_selected_changed)

        self.greeting = Label(text=self.label_value)

        self.greeting.pack()
        self.window.geometry("800x600+300+100")
        self.window.mainloop()

    def on_selected_changed(self, event):
        self.label_value.set(self.cb_value.get())