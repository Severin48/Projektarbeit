import tkinter as tk
from tkinter import ttk
from tkinter import *
from ttkthemes import ThemedTk
from PIL import ImageTk, Image

width = 900 # 720
height = 600 # 512
small = height/20


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

        self.mainframe = Frame(master=self.master, bg="green")  # , width=width, height=height)
        self.mainframe.rowconfigure(0, weight=1)  # Top bar
        self.mainframe.rowconfigure(1, weight=29)  # Shop Listing & Cart
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.grid(row=0, column=0, sticky="WENS")

        top_bar_height = small
        self.top_bar = Frame(master=self.mainframe, bg="black")
        # self.top_bar.grid_columnconfigure(2, minsize=width)
        self.top_bar.grid_columnconfigure(0, weight=2)
        self.top_bar.grid_columnconfigure(1, weight=2)
        self.top_bar.grid_columnconfigure(2, weight=14)
        self.top_bar.grid_columnconfigure(3, weight=1)
        self.top_bar.grid_columnconfigure(4, weight=1)
        # self.top_bar.grid_rowconfigure(0, weight=1, height=top_bar_height)
        self.top_bar.grid_rowconfigure(0, weight=1)
        self.top_bar.grid(row=0, column=0, sticky="WENS")
        # self.top_bar.grid(row=0, column=0, columnspan=2, sticky="WENS")
        # TODO: Shop contents col=0, cart col=1 --> Analog bei Lib

        self.fr_shop_label = Frame(master=self.top_bar, bg="black")
        self.fr_shop_label.grid(row=0, column=0, sticky="W", padx=5)
        self.shop_label = ttk.Label(self.fr_shop_label, text="SHOP", style="TB.TLabel")
        self.shop_label.grid(row=0, column=0, sticky="W", padx=5)
        self.shop_label.bind("<Button-1>", self.open_shop)

        self.fr_lib_label = Frame(master=self.top_bar, bg="black")
        self.fr_lib_label.grid(row=0, column=1, sticky="W", padx=5)
        self.lib_label = ttk.Label(self.fr_lib_label, text="BIBLIOTHEK", style="TB.TLabel")
        self.lib_label.grid(row=0, column=0, sticky="W", padx=5)
        self.lib_label.bind("<Button-1>", self.open_lib)

        self.fr_placeholder_label = Frame(master=self.top_bar, bg="black")
        self.fr_placeholder_label.grid(row=0, column=2, sticky="WENS", padx=5)
        self.placeholder_label = ttk.Label(self.fr_placeholder_label, style="TB.TLabel", background="black")
        self.placeholder_label.grid(row=0, column=0, sticky="WENS")

        self.fr_profile_label = Frame(master=self.top_bar, bg="black")
        self.fr_profile_label.grid(row=0, column=3, sticky="E", padx=5)
        self.profile_label = ttk.Label(self.fr_profile_label, text="S1mple")
        self.profile_label.grid(row=0, column=0, sticky="E")

        self.fr_balance_label = Frame(master=self.top_bar, bg="black")
        self.fr_balance_label.grid(row=0, column=4, sticky="E", padx=5)
        self.balance_label = ttk.Label(self.fr_balance_label, text=str(balance) + "€")
        self.balance_label.grid(row=0, column=0, sticky="E")

        # ====================================== SHOP PAGE ======================================

        self.shop_page = Frame(master=self.mainframe, bg="black")
        self.shop_page.columnconfigure(0, weight=7)
        self.shop_page.columnconfigure(1, weight=3)
        self.shop_page.rowconfigure(0, weight=1)
        self.shop_page.rowconfigure(1, weight=29)

        self.sorting_bar_sh = Frame(master=self.shop_page, bg="black")

        self.game_listings_frame = ScrollableFrame(container=self.shop_page)

        self.cart = Frame(master=self.shop_page, bg="blue")

        self.sort_by_price_label = ttk.Label(self.sorting_bar_sh, text="Sortieren nach Preis", width=20,
                                             style="TB.TLabel")
        self.sort_by_price_label.bind("<Button-1>", self.sort_by_price)

        self.sort_shop_by_name_label = ttk.Label(self.sorting_bar_sh, text="Sortieren nach Name", width=20,
                                            style="TB.TLabel")
        self.sort_shop_by_name_label.bind("<Button-1>", self.sort_shop_by_name)

        self.open_shop(event=None)  # Show the shop on launch

    def open_shop(self, event):
        # if self.showing != "shop":
            # self.lib_page.grid_forget()
            # login.grid_forget() # TODO: Wieder aktivieren

        self.shop_page.grid(row=1, column=0, sticky="wens")

        self.sorting_bar_sh.grid(row=0, column=0, sticky="wens")

        self.game_listings_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)

        self.cart.grid(row=1, column=1, sticky="wens")

        self.sort_by_price_label.grid(row=0, column=1, sticky="w")
        self.sort_by_price_label.configure(font=("arial", 12))

        self.sort_shop_by_name_label.grid(row=0, column=1, sticky="w")
        self.sort_shop_by_name_label.configure(font=("arial", 12))

        for i in range(60):
            ttk.Label(self.game_listings_frame.scrollable_frame, text="Sample shop label").pack()

        # print("Opening shop")
        self.showing = "shop"

    def open_lib(self, event):
        self.shop_page.grid_forget()
        self.showing = "lib"

        self.lib_page.grid(row=1, column=0, sticky="w")

        self.sorting_bar_lib.grid_columnconfigure(2, minsize=width)
        self.sorting_bar_lib.grid(rowspan=1, columnspan=8, sticky="we")

        self.sort_by_playtime_label.grid(row=0, column=1, sticky="w")
        self.sort_by_playtime_label.configure(font=("arial", 12))

        self.sort_lib_by_name_label.grid(row=0, column=1, sticky="w")
        self.sort_lib_by_name_label.configure(font=("arial", 12))

        for i in range(60):
            ttk.Label(self.game_library_frame.scrollable_frame, text="Sample library label").pack()

        self.game_library_frame.grid(row=1, column=0, rowspan=4, columnspan=4, sticky='nsew')

        print("Opening library")

    def open_login(self, event):
        print("Opening login screen")

    def sort_by_price(self, event):
        # TODO: Hier gute Fehlermeldungen printen je nach Wert den man zurückbekommt oder je nach Error
        print("Nach Preis Sortieren")
        self.sort_by_price_label.grid_forget()
        self.sort_shop_by_name_label.grid()

    def sort_shop_by_name(self, event):
        # TODO: Hier gute Fehlermeldungen printen je nach Wert den man zurückbekommt oder je nach Error
        print("Nach Name Sortieren")
        self.sort_shop_by_name_label.grid_forget()
        self.sort_by_price_label.grid()

    def sort_lib_by_name(self, event):
        # TODO: Hier gute Fehlermeldungen printen je nach Wert den man zurückbekommt oder je nach Error
        print("Nach Name Sortieren")
        self.sort_lib_by_name_label.grid_forget()
        self.sort_by_playtime_label.grid()

    def sort_by_playtime(self, event):
        self.sort_by_playtime_label.grid_forget()
        self.sort_lib_by_name_label.grid()


    # def browse_game_listings(self):
    #     # TODO: Mit event prüfen ob nach oben oder unten gescrollt wird?
    #     pass


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        # TODO: Refactor
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
    # root.resizable(False, False) TODO: Wieder einsetzen?
    win_size = str(width) + "x" + str(height)
    root.geometry(win_size)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # root.grid_propagate(0) TODO: Wieder einsetzen?

    root.mainloop()


if __name__ == '__main__':
    main()
