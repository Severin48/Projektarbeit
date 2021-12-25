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
        self.showing = ""

        self.mainframe = Frame(master=self.master, height=height, bg="black")
        self.mainframe.grid(rowspan=1, columnspan=8, sticky="we")

        # ====================================== TOP BAR ======================================
        self.top_bar_height = 20
        self.top_bar = Frame(master=self.mainframe, height=self.top_bar_height, bg="black")
        self.top_bar.grid_columnconfigure(2, minsize=width)
        self.top_bar.grid(rowspan=1, columnspan=8, sticky="we")  # sticky="we" so the bar starts on the left side

        self.shop_label = ttk.Label(self.top_bar, text="SHOP", width=8, style="TB.TLabel")
        self.shop_label.grid(row=0, column=0, sticky="w")
        self.shop_label.bind("<Button-1>", self.open_shop)

        self.lib_label = ttk.Label(self.top_bar, text="BIBLIOTHEK", width=14, style="TB.TLabel")
        self.lib_label.grid(row=0, column=1, sticky="w")
        self.lib_label.bind("<Button-1>", self.open_lib)

        self.profile_label = ttk.Label(self.top_bar, text="S1mple", width=8)
        self.profile_label.grid(row=0, column=5, sticky="e")

        pad_balance = 2
        self.balance_label = ttk.Label(self.top_bar, text=str(balance) + "€", width=len(str(balance))+pad_balance)
        self.balance_label.grid(row=0, column=6, sticky="e")

        self.logout_label = ttk.Label(self.top_bar, text="Logout", width=8)  # TODO: Symbol (Tür)
        self.logout_label.grid(row=0, column=7, sticky="e")
        self.logout_label.bind("<Button-1>", self.open_login)

        # self.close_button = Button(master, text="x", command=master.quit)
        # self.close_button.pack()

        # self.shop_page = Frame(master=master, height=height-self.top_bar_height, bg="black")

        # ====================================== SHOP PAGE ======================================

        shop_height = height - self.top_bar_height
        self.shop_page = Frame(master=self.mainframe, height=shop_height, bg="black")
        sorting_bar_height = 20
        self.sorting_bar = Frame(master=self.shop_page, height=sorting_bar_height, bg="black")

        self.sort_by_price_label = ttk.Label(self.sorting_bar, text="Sortieren nach Preis", width=20,
                                             style="TB.TLabel")
        self.sort_by_price_label.bind("<Button-1>", self.sort_by_price)

        self.sort_by_name_label = ttk.Label(self.sorting_bar, text="Sortieren nach Name", width=20,
                                             style="TB.TLabel")
        self.sort_by_name_label.bind("<Button-1>", self.sort_by_name)

        # self.game_listings_frame = ttk.Frame(master=self.shop_page, height=shop_height - sorting_bar_height,
        # bg="black")
        # self.game_listings_frame = ttk.Frame(master=self.shop_page, height=shop_height - sorting_bar_height)
        self.game_listings_frame = ScrollableFrame(container=self.shop_page, height=shop_height - sorting_bar_height,
                                                   width=0.4*width)
        self.game_listings_frame.pack_propagate(False)

        # Je game listing jeweils noch Frame

        # self.game_entries = []
        # self.game_entry

    def open_shop(self, event):
        if self.showing != "shop":
            # lib.grid_forget()
            # login.grid_forget()

            self.shop_page.grid(row=1, column=0, sticky="w")

            self.sorting_bar.grid_columnconfigure(2, minsize=width)
            self.sorting_bar.grid(rowspan=1, columnspan=8, sticky="we")

            self.sort_by_price_label.grid(row=0, column=1, sticky="w")
            self.sort_by_price_label.configure(font=("arial", 12))

            self.sort_by_name_label.grid(row=0, column=1, sticky="w")
            self.sort_by_name_label.configure(font=("arial", 12))

            for i in range(100):
                ttk.Label(self.game_listings_frame.scrollable_frame, text="Sample scrolling label").pack()

            self.game_listings_frame.grid(row=1, column=0, rowspan=4, columnspan=4, sticky='nsew')

            print("Opening shop")
            self.showing = "shop"

    def open_lib(self, event):
        self.shop_page.grid_forget()
        self.showing = "lib"
        print("Opening library")

    def open_login(self, event):
        print("Opening login screen")

    def sort_by_price(self, event):
        # TODO: Hier gute Fehlermeldungen printen je nach Wert den man zurückbekommt oder je nach Error
        print("Nach Preis Sortieren")
        self.sort_by_price_label.grid_forget()
        self.sort_by_name_label.grid()

    def sort_by_name(self, event):
        # TODO: Hier gute Fehlermeldungen printen je nach Wert den man zurückbekommt oder je nach Error
        print("Nach Name Sortieren")
        self.sort_by_name_label.grid_forget()
        self.sort_by_price_label.grid()


    # def browse_game_listings(self):
    #     # TODO: Mit event prüfen ob nach oben oder unten gescrollt wird?
    #     pass

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


def main():
    # root = Tk()
    root = ThemedTk()
    style = ttk.Style()
    style.theme_use('clam')
    # print(style.theme_names())
    # style.configure("C.TButton", foreground="white", background="black", relief="groove")
    # style.configure("TButton", foreground="green", background="black")
    style.configure("TB.TLabel", foreground="white", background="black", anchor="center", font=('arial', 20))
    style.configure(root, background="black", foreground="white")
    dampf = Dampf(root, get_balance())
    # canvas = Canvas(root, width=width, height=height)
    # canvas.grid()
    # canvas.grid(columnspan=3)
    root.resizable(False, False)
    win_size = str(width) + "x" + str(height)
    root.geometry(win_size)
    root.grid_propagate(0)

    root.mainloop()


if __name__ == '__main__':
    main()
