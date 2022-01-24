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

        # self.mainframe = Frame(master=self.master, height=height, width=width, bg="black")
        self.mainframe = Frame(master=self.master, bg="black")
        self.mainframe.rowconfigure(0, weight=1)  # Top bar
        self.mainframe.rowconfigure(1, weight=19)  # Shop Listing & Cart
        # self.mainframe.columnconfigure(0, weight=1)  # Shop label
        # self.mainframe.columnconfigure(1, weight=1)  # Library label
        # self.mainframe.columnconfigure(2, weight=15)  # space between shop,lib & username, €(, logout)
        # # TODO: Kein Logout? --> bei C# ist keiner
        # self.mainframe.columnconfigure(3, weight=1)  # Username Label
        # self.mainframe.columnconfigure(4, weight=1)  # Balance label
        self.mainframe.grid(sticky="WENS")

        # ====================================== TOP BAR ======================================

        top_bar_height = small
        self.top_bar = Frame(master=self.mainframe, height=top_bar_height, bg="black")
        # self.top_bar.grid_columnconfigure(2, minsize=width)
        self.top_bar.grid_columnconfigure(0, weight=2)
        self.top_bar.grid_columnconfigure(1, weight=2)
        self.top_bar.grid_columnconfigure(2, weight=14)
        self.top_bar.grid_columnconfigure(3, weight=1)
        self.top_bar.grid_columnconfigure(4, weight=1)
        self.top_bar.grid_rowconfigure(0, weight=1)
        # self.top_bar.grid(rowspan=1, columnspan=5, row=0, column=0, sticky="WENS")
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="WENS") # TODO: Shop contents col=0, cart col=1 --> Analog bei Lib
        # self.top_bar.grid(row=0, column=0, sticky="WENS", columnspan=5, rowspan=1)

        # self.shop_label = ttk.Label(self.top_bar, text="SHOP", width=8, style="TB.TLabel", background="green")
        self.shop_label = ttk.Label(self.top_bar, text="SHOP", style="TB.TLabel")
        self.shop_label.grid(row=0, column=0, sticky="wens")
        self.shop_label.bind("<Button-1>", self.open_shop)

        # self.lib_label = ttk.Label(self.top_bar, text="BIBLIOTHEK", width=14, style="TB.TLabel")
        self.lib_label = ttk.Label(self.top_bar, text="BIBLIOTHEK", style="TB.TLabel")
        self.lib_label.grid(row=0, column=1, sticky="wens")
        self.lib_label.bind("<Button-1>", self.open_lib)

        # self.placeholder_label = ttk.Label(self.top_bar, text="", width=14, style="TB.TLabel")
        self.placeholder_label = ttk.Label(self.top_bar, style="TB.TLabel", background="green")
        self.placeholder_label.grid(row=0, column=2, sticky="wens")

        # self.profile_label = ttk.Label(self.top_bar, text="S1mple", width=8)
        self.profile_label = ttk.Label(self.top_bar, text="S1mple")
        self.profile_label.grid(row=0, column=3, sticky="wens")

        pad_balance = 2
        # self.balance_label = ttk.Label(self.top_bar, text=str(balance) + "€", width=len(str(balance))+pad_balance)
        self.balance_label = ttk.Label(self.top_bar, text=str(balance) + "€")
        self.balance_label.grid(row=0, column=4, sticky="wens")

        # self.logout_label = ttk.Label(self.top_bar, text="Logout", width=8)  # TODO: Symbol (Tür)
        # self.logout_label.grid(row=0, column=7, sticky="e")  # TODO: Logout/Login benötigt?
        # self.logout_label.bind("<Button-1>", self.open_login)

        # self.close_button = Button(master, text="x", command=master.quit)
        # self.close_button.pack()

        # self.shop_page = Frame(master=master, height=height-self.top_bar_height, bg="black")

        # ====================================== SHOP PAGE ======================================

        shop_height = height - top_bar_height
        self.shop_page = Frame(master=self.mainframe, height=shop_height, bg="black")
        #
        # self.shop_page.grid_columnconfigure(0, minsize=width)
        # self.shop_page.resizable = False
        # self.top_bar.grid(rowspan=1, columnspan=8, sticky="we", row=1)

        sorting_bar_height = small

        self.sorting_bar_sh = Frame(master=self.shop_page, height=sorting_bar_height, bg="black")

        self.sort_by_price_label = ttk.Label(self.sorting_bar_sh, text="Sortieren nach Preis", width=20,
                                             style="TB.TLabel")
        self.sort_by_price_label.bind("<Button-1>", self.sort_by_price)

        self.sort_shop_by_name_label = ttk.Label(self.sorting_bar_sh, text="Sortieren nach Name", width=20,
                                            style="TB.TLabel")
        self.sort_shop_by_name_label.bind("<Button-1>", self.sort_shop_by_name)

        # self.game_listings_frame = ttk.Frame(master=self.shop_page, height=shop_height - sorting_bar_height,
        # bg="black")
        # self.game_listings_frame = ttk.Frame(master=self.shop_page, height=shop_height - sorting_bar_height)
        game_listings_height = shop_height - sorting_bar_height
        # self.game_listings_frame = ScrollableFrame(container=self.shop_page, height=game_listings_height,
        #                                            width=0.8*width)
        self.game_listings_frame = ScrollableFrame(container=self.shop_page)

        # TODO: Für alle rowconfigure und columnconfigure
        # self.game_listings_frame.pack_propagate(False)

        # Je game listing jeweils noch Frame

        # self.game_entries = []
        # self.game_entry
        self.open_shop(event=None) # Show the shop on launch

        # ====================================== LIB PAGE ======================================

        self.lib_page = Frame(master=self.mainframe, height=shop_height, bg="black")

        self.sorting_bar_lib = Frame(master=self.lib_page, height=sorting_bar_height, bg="black")

        self.sort_by_playtime_label = ttk.Label(self.sorting_bar_lib, text="Sortieren nach Spielzeit", width=20,
                                                style="TB.TLabel")
        self.sort_by_playtime_label.bind("<Button-1>", self.sort_by_playtime)

        self.sort_lib_by_name_label = ttk.Label(self.sorting_bar_lib, text="Sortieren nach Name", width=20,
                                            style="TB.TLabel")
        self.sort_lib_by_name_label.bind("<Button-1>", self.sort_lib_by_name)

        self.game_library_frame = ScrollableFrame(container=self.lib_page, height=game_listings_height,
                                                   width=0.4*width)

    def open_shop(self, event):
        if self.showing != "shop":
            self.lib_page.grid_forget()
            # login.grid_forget()

        self.shop_page.grid(row=1, column=0, sticky="wens")

        self.sorting_bar_sh.grid_columnconfigure(2, minsize=width)
        self.sorting_bar_sh.grid(rowspan=1, columnspan=8, sticky="we")

        self.sort_by_price_label.grid(row=0, column=1, sticky="w")
        self.sort_by_price_label.configure(font=("arial", 12))

        self.sort_shop_by_name_label.grid(row=0, column=1, sticky="w")
        self.sort_shop_by_name_label.configure(font=("arial", 12))

        for i in range(60):
            ttk.Label(self.game_listings_frame.scrollable_frame, text="Sample shop label").pack()

        self.game_listings_frame.grid(row=1, column=0, rowspan=1, columnspan=6, sticky='nsew')

        print("Opening shop")
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
    # root.grid_propagate(0) TODO: Wieder einsetzen?

    root.mainloop()


if __name__ == '__main__':
    main()
