from tkinter import *

# To find out what configuration options are available on any widget, call its configure() method, which returns a
# dictionary containing a variety of information
# about each object, including its default and current values. Use keys() to get just the names of each option.
# btn = ttk.Button(frm, ...)
# print(btn.configure().keys())

# Use the config() method to update multiple attrs subsequent to object creation btn.config(fg="red", bg="blue")

# The pack() method can be called with keyword-option/value pairs that control where the widget is to appear within its
# container, and how it is to behave when the main application window is resized. Here are some examples:

# fred.pack()                     # defaults to side = "top"
# fred.pack(side="left")
# fred.pack(expand=1)

# Dialoge/Eingaben https://docs.python.org/3/library/dialog.html

# Theme: https://docs.python.org/3/library/tkinter.ttk.html --> Imports richtig machen

library = Tk()
store = Tk()


if __name__ == '__main__':
    window = Tk()

    window.geometry("720x480")

    window.configure(background="black") # --> oder eben hex code der dem richtigen entspricht

    # images/pictures
    # photo1 = PhotoImage(file="game1.gif") # gif anscheinend besser als png -- was ist mit jpg?
    # Label(root, image=photo1, bg="black").grid(row=0, column=0, sticky=E)

    # Label fg = foreground --> aber eigentlich font. font="none... " --> Arial
    print("window1")
    # Label(root, text="W1 hier", bg="black", fg="white", font="none 12 bold").grid(row=0, column=0, sticky=E)
    Label(window, text="W1 hier", bg="black", fg="white", font="none 12 bold").pack()
    # Label(root, text="Window1 hier", bg="black", fg="white", font="none 12 bold").grid(row=0, column=1, sticky=E)
    Label(window, text="Window1 hier", bg="black", fg="white", font="none 12 bold").pack()
    # Button(root, )
    # btn = Button(window, text="window2", command=switch_page, fg="white", bg="black")
    # btn.grid(row=1, column=0, sticky=E)
    # btn.pack()
    # print("window2")
    # Label(window, text="Window2 hier", bg="black", fg="white", font="none 12 bold").grid(row=0, column=0, sticky=E)
    # Label(window, text="Window2 hier", bg="black", fg="white", font="none 12 bold").grid(row=0, column=1, sticky=E)

    window.mainloop()
