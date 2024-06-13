from tkinter import *
import tkinter.ttk as ttk

class Application:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("800x600+300+100")
        self.window.title("Projekt BSK")

        options = ["Szyfrowanie", "Deszyfrowanie"]
        self.variable = StringVar(self.window)
        self.variable.set(options[0])

        #w = OptionMenu(self.window, self.variable, *options)
        #w.place(x=300, y=100)
        #w.size()
        #w.pack()

        #button = Button(self.window, text="OK", command=self.ok)
        #button.place(x=300, y=500)



        self.window.mainloop()

    def ok(self):
        print("value is:" + self.variable.get())

if __name__ == "__main__":
    app = Application()