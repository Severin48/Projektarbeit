import tkinter as tk
from tkinter import ttk
from tkinter import *
from ttkthemes import ThemedTk
from PIL import ImageTk, Image

width = 900 # 720
height = 600 # 512
small = height/20

act_dark = "#252737"
pas_dark = "#343247"

# TODO: Typing


class Game:
    # TODO: Doc welche Einheiten/Typen z.B. Playtime in minuten
    def __init__(self, name, price, genre, platforms, discounted, playtime): # , image
        self.name = name
        self.price = price
        self.genre = genre
        self.platforms = platforms
        self.discounted = discounted
        self.playtime = playtime


def get_balance():
    balance = 1.60384572
    balance = round(balance, 2)
    return '{:.2f}'.format(balance)


class Dampf:
    def __init__(self, master, style, balance):
        self.master = master
        self.style = style
        self.balance = balance
        master.title("Dampf")
        self.showing = ""
        self.shop_games = set()
        self.lib_games = set()
        self.cart_games = set()

        self.shop_games.add(Game("Ruf der Pflicht: Moderne Kriegskunst 2", 59.99, ["First-person shooter", "Action"],
                            ["Windows"], False, 0))
        self.shop_games.add(Game("Gegenschlag: Globale Offensive", 0, ["FPS", "Tactical shooter"],
                            ["Windows", "Linux"], False, 101880))

        self.shop_games.add(Game("The Älteren Rollen: Himmelsrand", 0, ["RPG", "Fantasy"],
                                 ["Windows", "Linux"], False, 48920))

        self.shop_games.add(Game("Gothisch 2: Die Nacht des Raben", 0, ["RPG", "Fantasy"],
                                 ["Windows", "Linux"], False, 48920))

        self.mainframe = Frame(master=self.master, bg=pas_dark)  # , width=width, height=height)
        self.mainframe.rowconfigure(0, weight=1)  # Top bar
        self.mainframe.rowconfigure(1, weight=29)  # Shop Listing & Cart
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.grid(row=0, column=0, sticky="WENS")

        top_bar_height = small
        self.top_bar = Frame(master=self.mainframe, bg=pas_dark)
        # self.top_bar.grid_columnconfigure(2, minsize=width)
        self.top_bar.columnconfigure(0, weight=2)
        self.top_bar.columnconfigure(1, weight=2)
        self.top_bar.columnconfigure(2, weight=14)
        self.top_bar.columnconfigure(3, weight=1)
        self.top_bar.columnconfigure(4, weight=1)
        # self.top_bar.grid_rowconfigure(0, weight=1, height=top_bar_height)
        self.top_bar.rowconfigure(0, weight=1)
        self.top_bar.grid(row=0, column=0, sticky="WENS")
        # self.top_bar.grid(row=0, column=0, columnspan=2, sticky="WENS")
        # TODO: Shop contents col=0, cart col=1 --> Analog bei Lib

        self.fr_shop_label = Frame(master=self.top_bar, bg=pas_dark)
        self.fr_shop_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)
        self.shop_label = ttk.Label(self.fr_shop_label, text="SHOP", style="TB.TLabel")
        self.shop_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)
        self.shop_label.bind("<Button-1>", self.open_shop)

        self.fr_lib_label = Frame(master=self.top_bar, bg=pas_dark)
        self.fr_lib_label.grid(row=0, column=1, sticky="W", padx=5, pady=5)
        self.lib_label = ttk.Label(self.fr_lib_label, text="BIBLIOTHEK", style="TB.TLabel")
        self.lib_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)
        self.lib_label.bind("<Button-1>", self.open_lib)

        self.fr_placeholder_label = Frame(master=self.top_bar, bg=pas_dark)
        self.fr_placeholder_label.grid(row=0, column=2, sticky="WENS", padx=5, pady=5)
        self.placeholder_label = ttk.Label(self.fr_placeholder_label, style="TB.TLabel", background=pas_dark)
        self.placeholder_label.grid(row=0, column=0, sticky="WENS")

        self.fr_profile_label = Frame(master=self.top_bar, bg=pas_dark)
        self.fr_profile_label.grid(row=0, column=3, sticky="E", padx=5, pady=5)
        self.profile_label = ttk.Label(self.fr_profile_label, text="S1mple")
        self.profile_label.grid(row=0, column=0, sticky="E", padx=5, pady=5)

        self.fr_balance_label = Frame(master=self.top_bar, bg=pas_dark)
        self.fr_balance_label.grid(row=0, column=4, sticky="E", padx=5, pady=5)
        self.balance_label = ttk.Label(self.fr_balance_label, text=str(balance) + "€")
        self.balance_label.grid(row=0, column=0, sticky="E", padx=5, pady=5)
        self.balance_label.bind("<Button-1>", self.open_funds)

        # ====================================== LIB PAGE ======================================

        self.lib_page = Frame(master=self.mainframe, bg=pas_dark)
        self.lib_page.columnconfigure(0, weight=7)
        self.lib_page.columnconfigure(1, weight=3)
        self.lib_page.rowconfigure(0, weight=1)
        self.lib_page.rowconfigure(1, weight=29)

        self.sorting_bar_lib = Frame(master=self.lib_page, bg=pas_dark)

        self.info_tab = Frame(master=self.lib_page, bg="blue")

        self.sort_by_playtime_label = ttk.Label(self.sorting_bar_lib, text="Sortieren nach Spielzeit", width=20,
                                                style="TB.TLabel")
        self.sort_by_playtime_label.bind("<Button-1>", self.sort_by_playtime)

        self.sort_lib_by_name_label = ttk.Label(self.sorting_bar_lib, text="Sortieren nach Name", width=20,
                                            style="TB.TLabel")
        self.sort_lib_by_name_label.bind("<Button-1>", self.sort_lib_by_name)

        self.game_library_frame = ScrollableFrame(container=self.lib_page)

        for i in range(20):
            ttk.Label(self.game_library_frame.scrollable_frame, text="Sample library label").pack()

        # ====================================== Adding Funds ======================================

        style.configure("Addfds.TLabel", foreground="white", background="green", anchor="center", font=('arial', 20))

        self.funds_frame = Frame(master=self.mainframe, bg=pas_dark)
        self.funds_frame.columnconfigure(0, weight=4)
        self.funds_frame.columnconfigure(1, weight=1)
        for i in range(5):
            self.funds_frame.rowconfigure(i, weight=1)
        self.fr_add_five = Frame(master=self.funds_frame, bg=act_dark)
        self.fr_add_ten = Frame(master=self.funds_frame, bg=act_dark)
        self.fr_add_twentyfive = Frame(master=self.funds_frame, bg=act_dark)
        self.fr_add_fifty = Frame(master=self.funds_frame, bg=act_dark)
        self.fr_add_hundred = Frame(master=self.funds_frame, bg=act_dark)

        # TODO: Padding dazwischen

        self.desc_five = ttk.Label(self.fr_add_five, text="5,--€", # \nMinimaler Aufladebetrag
                                   style="TB.TLabel")
        self.desc_five.configure(font=('arial', 14), background=act_dark)

        self.desc_ten = ttk.Label(self.fr_add_ten, text="10,--€",
                                   style="TB.TLabel")
        self.desc_ten.configure(font=('arial', 14), background=act_dark)

        self.desc_twentyfive = ttk.Label(self.fr_add_twentyfive, text="25,--€",
                                   style="TB.TLabel")
        self.desc_twentyfive.configure(font=('arial', 14), background=act_dark)

        self.desc_fifty = ttk.Label(self.fr_add_fifty, text="50,--€",
                                   style="TB.TLabel")
        self.desc_fifty.configure(font=('arial', 14), background=act_dark)

        self.desc_hundred = ttk.Label(self.fr_add_hundred, text="100,--€",
                                   style="TB.TLabel")
        self.desc_hundred.configure(font=('arial', 14), background=act_dark)

        self.add_five = ttk.Label(self.fr_add_five, text="5,--€ Guthaben aufladen", style="Addfds.TLabel")
        self.add_five.bind("<Button-1>", lambda event, x=5: self.add_funds(event, x))

        self.add_ten = ttk.Label(self.fr_add_ten, text="10,--€ Guthaben aufladen", style="Addfds.TLabel")
        self.add_ten.bind("<Button-1>", lambda event, x=10: self.add_funds(event, x))

        self.add_twentyfive = ttk.Label(self.fr_add_twentyfive, text="25,--€ Guthaben aufladen", style="Addfds.TLabel")
        self.add_twentyfive.bind("<Button-1>", lambda event, x=25: self.add_funds(event, x))

        self.add_fifty = ttk.Label(self.fr_add_fifty, text="50,--€ Guthaben aufladen", style="Addfds.TLabel")
        self.add_fifty.bind("<Button-1>", lambda event, x=50: self.add_funds(event, x))

        self.add_hundred = ttk.Label(self.fr_add_hundred, text="100,--€ Guthaben aufladen", style="Addfds.TLabel")
        self.add_hundred.bind("<Button-1>", lambda event, x=100: self.add_funds(event, x))

        self.fr_balance_big = Frame(master=self.funds_frame, bg=act_dark)
        self.balance_big = ttk.Label(self.fr_balance_big, text="Aktuelles Guthaben", style="TB.TLabel",
                                     background=act_dark)

        self.balance_value_label = ttk.Label(self.fr_balance_big, text=str(get_balance()) + "€", style="TB.TLabel",
                                             background=act_dark)
        self.balance_value_label.configure(font=("arial", 12))

        # ====================================== SHOP PAGE ======================================

        self.shop_page = Frame(master=self.mainframe, bg=pas_dark)
        self.shop_page.columnconfigure(0, weight=7)
        self.shop_page.columnconfigure(1, weight=3)
        self.shop_page.rowconfigure(0, weight=1)
        self.shop_page.rowconfigure(1, weight=29)

        self.sorting_bar_sh = Frame(master=self.shop_page, bg=pas_dark)

        self.game_listings_frame = ScrollableFrame(container=self.shop_page) # TODO: Scrollable mit mousewheel machen


        # for i in range(20):
        #     ttk.Label(self.game_listings_frame.scrollable_frame, text="Sample shop label").pack()

        for game in self.shop_games:
            GameFrame(container=self.game_listings_frame.scrollable_frame, game=game).pack()

        self.cart = Frame(master=self.shop_page, bg="blue")

        self.sort_by_price_label = ttk.Label(self.sorting_bar_sh, text="Sortieren nach Preis", width=20,
                                             style="TB.TLabel")
        self.sort_by_price_label.bind("<Button-1>", self.sort_by_price)

        self.sort_shop_by_name_label = ttk.Label(self.sorting_bar_sh, text="Sortieren nach Name", width=20,
                                            style="TB.TLabel")
        self.sort_shop_by_name_label.bind("<Button-1>", self.sort_shop_by_name)

        self.open_shop(event=None)  # Show the shop on launch

    def open_shop(self, event):
        if self.showing != "shop":
            self.shop_label.configure(font=("arial", 20, "bold"), background=act_dark)
            self.lib_label.configure(font=('arial', 20), background=pas_dark)
            self.balance_label.configure(background=pas_dark)
            # self.top_bar.grid(row=0, column=0, rowspan=1, sticky="WENS")
            # self.top_bar.grid_rowconfigure(rowspan=1)

            self.lib_page.grid_forget()
            self.funds_frame.grid_forget()
            # login.grid_forget() # TODO: Login weg?

            self.shop_page.grid(row=1, column=0, sticky="wens")

            self.sorting_bar_sh.grid(row=0, column=0, sticky="wens")

            self.game_listings_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)

            self.cart.grid(row=1, column=1, sticky="wens")

            self.sort_by_price_label.grid(row=0, column=1, sticky="w")
            self.sort_by_price_label.configure(font=("arial", 12))

            self.sort_shop_by_name_label.grid(row=0, column=1, sticky="w")
            self.sort_shop_by_name_label.configure(font=("arial", 12))

            for game in self.shop_games:
                GameFrame(container=self.game_listings_frame.scrollable_frame, game=game).pack()

            # print("Opening shop")
            self.showing = "shop"

    def open_lib(self, event):
        self.shop_page.grid_forget()
        self.funds_frame.grid_forget()
        self.lib_label.configure(font=("arial", 20, "bold"), background=act_dark)
        self.shop_label.configure(font=('arial', 20), background=pas_dark)
        self.balance_label.configure(background=pas_dark)
        # self.top_bar.grid_rowconfigure(rowspan=1)

        self.lib_page.grid(row=1, column=0, sticky="wens")

        self.sorting_bar_lib.grid(row=0, column=0, sticky="wens")

        self.info_tab.grid(row=1, column=1, sticky="wens")

        self.sort_by_playtime_label.grid(row=0, column=1, sticky="w")
        self.sort_by_playtime_label.configure(font=("arial", 12))

        self.sort_lib_by_name_label.grid(row=0, column=1, sticky="w")
        self.sort_lib_by_name_label.configure(font=("arial", 12))

        self.game_library_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)

        self.showing = "lib"

        # print("Opening library")

    def open_funds(self, event):
        self.shop_page.grid_forget()
        self.lib_page.grid_forget()
        self.shop_label.configure(font=('arial', 20), background=pas_dark)
        self.lib_label.configure(font=('arial', 20), background=pas_dark)
        self.balance_label.configure(background=act_dark)
        # self.top_bar.grid_rowconfigure(rowspan=2) # TODO: Top bar shouldn't resize when clicking on funds and back

        self.funds_frame.grid(row=1, column=0, sticky="wens")
        self.fr_add_five.grid(row=0, column=0, sticky="wens")
        self.fr_add_ten.grid(row=1, column=0, sticky="wens")
        self.fr_add_twentyfive.grid(row=2, column=0, sticky="wens")
        self.fr_add_fifty.grid(row=3, column=0, sticky="wens")
        self.fr_add_hundred.grid(row=4, column=0, sticky="wens")

        self.desc_five.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.desc_five.place(anchor="center", relx=.1, rely=.5)
        self.desc_ten.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.desc_ten.place(anchor="center", relx=.1, rely=.5)
        self.desc_twentyfive.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.desc_twentyfive.place(anchor="center", relx=.1, rely=.5)
        self.desc_fifty.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.desc_fifty.place(anchor="center", relx=.1, rely=.5)
        self.desc_hundred.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.desc_hundred.place(anchor="center", relx=.1, rely=.5)

        self.add_five.grid(row=0, column=1, sticky="e", padx=10, pady=10)
        self.add_five.place(anchor="center", relx=.75, rely=.5)
        self.add_ten.grid(row=1, column=1, sticky="e", padx=10, pady=10)
        self.add_ten.place(anchor="center", relx=.75, rely=.5)
        self.add_twentyfive.grid(row=2, column=1, sticky="e", padx=10, pady=10)
        self.add_twentyfive.place(anchor="center", relx=.75, rely=.5)
        self.add_fifty.grid(row=3, column=1, sticky="e", padx=10, pady=10)
        self.add_fifty.place(anchor="center", relx=.75, rely=.5)
        self.add_hundred.grid(row=4, column=1, sticky="e", padx=10, pady=10)
        self.add_hundred.place(anchor="center", relx=.75, rely=.5)

        self.fr_balance_big.grid(row=0, column=1, sticky="wens", padx=10, pady=10)
        self.fr_balance_big.grid_propagate(0)
        self.balance_big.grid(padx=10, pady=10)
        self.balance_big.configure(font=('arial', 12))
        self.balance_big.place(anchor="c", relx=.5, rely=.1)

        self.balance_value_label.grid(padx=10, pady=10)
        self.balance_value_label.place(anchor="c", relx=.5, rely=.5)

        # TODO: Funds aktualisieren wenn sie sich ändern
        # TODO: Erklärung schreiben z.B. zum Aufladen von Guthaben auf den Betrag rechts oben klicken

        self.showing = "funds"

    def add_funds(self, event, amount):
        # TODO: von Studierenden zu implementieren
        print("Guthaben müsste {},--€ aufgeladen werden".format(amount))


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

    def get_shop_games(self):
        return self.shop_games


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


# class GameFrame(ttk.Frame):
#     def __init__(self, container, game, *args, **kwargs):
#         super().__init__(container, *args, **kwargs)
#         self.game = game
#
#         canvas = tk.Canvas(self)
#
#         self.game_frame = ttk.Frame(canvas)
#
#         self.game_frame.columnconfigure(0, weight=1) # Image
#         self.game_frame.columnconfigure(1, weight=3) # Name, Platforms, Genre
#         self.game_frame.columnconfigure(2, weight=1)
#
#         canvas.create_window((0, 0), window=self.game_frame, anchor="nw")
#
#         canvas.pack(side="left", fill="both", expand=True)

class GameFrame(ttk.Frame):
    def __init__(self, container, game, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.game = game

        canvas = tk.Canvas(self)

        self.game_frame = ttk.Frame(canvas)

        self.game_frame.columnconfigure(0, weight=1) # Image
        self.game_frame.columnconfigure(1, weight=3) # Name, Platforms, Genre
        self.game_frame.columnconfigure(2, weight=1)

        canvas.create_window((0, 0), window=self.game_frame, anchor="nw")

        self.l_name = ttk.Label(self.game_frame, text=game.name, style="TB.TLabel", background="blue")
        self.l_name.configure(font=('arial', 14))
        self.l_name.pack()

        canvas.pack(side="left", fill="both", expand=True)


def main():
    # root = Tk()
    root = ThemedTk()
    style = ttk.Style()
    style.theme_use('clam')
    # print(style.theme_names())
    # style.configure("C.TButton", foreground="white", background="black", relief="groove")
    # style.configure("TButton", foreground="green", background="black")
    style.configure("TB.TLabel", foreground="white", background=pas_dark, anchor="center", font=('arial', 20))
    style.configure(root, background=pas_dark, foreground="white")
    dampf = Dampf(root, style, get_balance())
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
