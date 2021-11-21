import tkinter as tk
from tkinter import ttk
from tkinter import *
from ttkthemes import ThemedTk
from PIL import ImageTk, Image

width = 720
height = 512


def get_balance():
    balance = 1.60384572
    balance = round(balance, 2)
    return '{:.2f}'.format(balance)


class Dampf:
    def __init__(self, master, balance):
        self.master = master
        self.balance = balance
        master.title("Dampf")

        # TODO: Label statt Button:  label.bind("<Button-1>",lambda e,url=url:open_url(url))

        top_bar = Frame(master=master, height=20, bg="black")
        top_bar.grid_columnconfigure(2, minsize=width)
        top_bar.grid(rowspan=1, columnspan=8, sticky="we")  # sticky="we" so the bar starts on the left side

        #self.shop_button = ttk.Button(top_bar, text="SHOP", width=10, command=self.open_shop)
        self.shop_label = ttk.Label(top_bar, text="SHOP", width=8, style="TB.TLabel")
        self.shop_label.grid(row=0, column=0, sticky="w")
        self.shop_label.bind("<Button-1>", self.open_shop)

        self.lib_label = ttk.Label(top_bar, text="BIBLIOTHEK", width=14, style="TB.TLabel")
        self.lib_label.grid(row=0, column=1, sticky="w")
        self.lib_label.bind("<Button-1>", self.open_lib)
        # self.top_bar_labels.append(self.lib_label)

        self.profile_label = ttk.Label(top_bar, text="S1mple", width=8)
        self.profile_label.grid(row=0, column=5, sticky="e")

        pad_balance = 2
        self.balance_label = ttk.Label(top_bar, text=str(balance) + "€", width=len(str(balance))+pad_balance)
        self.balance_label.grid(row=0, column=6, sticky="e")

        self.logout_label = ttk.Label(top_bar, text="Logout", width=8)  # TODO: Symbol (Tür)
        self.logout_label.grid(row=0, column=7, sticky="e")
        self.logout_label.bind("<Button-1>", self.open_login)

        # self.close_button = Button(master, text="x", command=master.quit)
        # self.close_button.pack()

    def open_shop(self, event):
        self.app = Shop(self.master)
        print("Opening shop")


    def open_lib(self, event):
        print("Opening library")

    def open_login(self, event):
        print("Opening login screen")


class Page(ttk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Shop(Page):
    def __init__(self, master):
        self.master = master

        sorting_bar = Frame(master=master, height=20, bg="black")
        sorting_bar.grid_columnconfigure(2, minsize=width)
        sorting_bar.grid_rowconfigure(2)
        sorting_bar.grid(rowspan=1, columnspan=8, sticky="we")

        self.sort_by_price_label = ttk.Label(sorting_bar, text="Sortieren nach Preis", width=20, style="TB.TLabel")
        self.sort_by_price_label.grid(row=0, column=1, sticky="w")
        self.sort_by_price_label.bind("<Button-1>", self.sort_by_price)

    def sort_by_price(self):
        pass


class Library(Page):
    def __init__(self, master):
        self.master = master


class Login(Page):
    def __init__(self, master):
        self.master = master


def main():
    # root = Tk()
    root = ThemedTk()
    style = ttk.Style()
    style.theme_use('clam')
    # print(style.theme_names())

    # style.configure("C.TButton", foreground="white", background="black", relief="groove")
    # style.configure("TButton", foreground="green", background="black")
    style.configure("TB.TLabel", foreground="white", background="black", anchor="center", font=('arial', 20))
    style.configure("TNotebook", foreground="white", background="black", fg="white", bg="black")
    style.configure(root, background="black", foreground="white")
    win_size = str(width) + "x" + str(height)
    root.geometry(win_size)
    tabControl = ttk.Notebook(root)

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)

    tabControl.add(tab1, text='Tab 1')
    tabControl.add(tab2, text='Tab 2')
    tabControl.pack(expand=1, fill="both")

    # dampf = Dampf(root, get_balance())
    # canvas = Canvas(root, width=width, height=height)
    # canvas.grid()
    root.resizable(False, False)
    root.mainloop()


if __name__ == '__main__':
    main()
