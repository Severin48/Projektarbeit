import tkinter as tk
from tkinter import ttk
from tkinter import *
from ttkthemes import ThemedTk
from PIL import ImageTk, Image

width = 900  # 720
height = 600  # 512
small = height/20

act_dark = "#2d384b"
pas_dark = "#1f232a"

# TODO: Typing


class Game:
    # TODO: Doc welche Einheiten/Typen z.B. Playtime in minuten
    def __init__(self, name, price, genre, platforms, playtime, img, owned=False, discounted=False):
        self.name = name
        self.price = price
        self.genre = genre
        self.platforms = platforms
        self.discounted = discounted
        self.playtime = playtime
        self.in_cart = False
        self.owned = owned
        self.img = ImageTk.PhotoImage(Image.open("imgs/" + img))

    def to_cart(self, event):
        print("Added {} to cart".format(self.name))
        self.in_cart = True

    def remove_from_cart(self, event):
        print("Removed {} from cart".format(self.name))
        self.in_cart = False


# def get_balance():
#     # balance = 1.60384572
#     balance = round(balance, 2)
#     return '{:.2f}'.format(balance)

# TODO: Wenn genug Funds vorhanden sind nicht auf AddFundsPage


class Dampf:
    def __init__(self, master, style):  # , balance):
        self.master = master
        self.style = style
        self.balance = 0  # alt: = balance
        master.title("Dampf")
        self.showing = ""
        self.all_games = []
        self.shop_games = []
        self.lib_games = []
        self.cart_games = []
        self.game_frames = []

        self.all_games.append(Game("Ruf der Pflicht: Moderne Kriegskunst 2", 59.99, ["First-person shooter", "Action"],
                                   ["Windows"], 0, "mw2.png", discounted=True))

        self.all_games.append(Game("Gegenschlag: Globale Offensive", 0, ["FPS", "Tactical shooter"],
                                   ["Windows", "Linux"], 101880, "cs.png", owned=True, discounted=True))

        self.all_games.append(Game("Die Älteren Rollen: Himmelsrand", 0, ["RPG", "Fantasy"],
                                   ["Windows", "Linux"], 48920, "tes5.png", discounted=True))

        self.all_games.append(Game("Gothisch 2: Die Nacht des Raben", 0, ["RPG", "Fantasy"],
                                   ["Windows", "Linux"], 48920, "g2.png"))

        for game in self.all_games:
            if not game.owned:
                self.shop_games.append(game)
            else:
                self.lib_games.append(game)

        # , width=width, height=height)
        self.mainframe = Frame(master=self.master, bg=pas_dark)
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
        self.shop_label = ttk.Label(
            self.fr_shop_label, text="SHOP", style="TB.TLabel")
        self.shop_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)
        self.shop_label.bind("<Button-1>", self.open_shop)

        self.fr_lib_label = Frame(master=self.top_bar, bg=pas_dark)
        self.fr_lib_label.grid(row=0, column=1, sticky="W", padx=5, pady=5)
        self.lib_label = ttk.Label(
            self.fr_lib_label, text="BIBLIOTHEK", style="TB.TLabel")
        self.lib_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)
        self.lib_label.bind("<Button-1>", self.open_lib)

        self.fr_placeholder_label = Frame(master=self.top_bar, bg=pas_dark)
        self.fr_placeholder_label.grid(
            row=0, column=2, sticky="WENS", padx=5, pady=5)
        self.placeholder_label = ttk.Label(
            self.fr_placeholder_label, style="TB.TLabel", background=pas_dark)
        self.placeholder_label.grid(row=0, column=0, sticky="WENS")

        self.fr_profile_label = Frame(master=self.top_bar, bg=pas_dark)
        self.fr_profile_label.grid(row=0, column=3, sticky="E", padx=5, pady=5)
        self.profile_label = ttk.Label(self.fr_profile_label, text="S1mple")
        self.profile_label.grid(row=0, column=0, sticky="E", padx=5, pady=5)

        self.fr_balance_label = Frame(master=self.top_bar, bg=pas_dark)
        self.fr_balance_label.grid(row=0, column=4, sticky="E", padx=5, pady=5)
        self.balance_label = ttk.Label(
            self.fr_balance_label, text=str(self.get_balance()) + "€")
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
                                                style="Sorting.TLabel")
        self.sort_by_playtime_label.bind("<Button-1>", self.sort_by_playtime)

        self.sort_lib_by_name_label = ttk.Label(self.sorting_bar_lib, text="Sortieren nach Name", width=20,
                                                style="Sorting.TLabel")
        self.sort_lib_by_name_label.bind("<Button-1>", self.sort_lib_by_name)

        self.game_library_frame = ScrollableFrame(container=self.lib_page)

        # ====================================== Adding Funds ======================================

        style.configure("Addfds.TLabel", foreground="white",
                        background="green", anchor="center", font=('arial', 20))

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

        self.desc_five = ttk.Label(self.fr_add_five, text="5,--€",  # \nMinimaler Aufladebetrag
                                   style="FundsAmount.TLabel")

        self.desc_ten = ttk.Label(self.fr_add_ten, text="10,--€",
                                  style="FundsAmount.TLabel")

        self.desc_twentyfive = ttk.Label(self.fr_add_twentyfive, text="25,--€",
                                         style="FundsAmount.TLabel")

        self.desc_fifty = ttk.Label(self.fr_add_fifty, text="50,--€",
                                    style="FundsAmount.TLabel")

        self.desc_hundred = ttk.Label(self.fr_add_hundred, text="100,--€",
                                      style="FundsAmount.TLabel")

        self.add_five = ttk.Label(
            self.fr_add_five, text="5,--€ Guthaben aufladen", style="Addfds.TLabel")
        self.add_five.bind("<Button-1>", lambda event,
                           x=5: self.add_funds(event, x))

        self.add_ten = ttk.Label(
            self.fr_add_ten, text="10,--€ Guthaben aufladen", style="Addfds.TLabel")
        self.add_ten.bind("<Button-1>", lambda event,
                          x=10: self.add_funds(event, x))

        self.add_twentyfive = ttk.Label(
            self.fr_add_twentyfive, text="25,--€ Guthaben aufladen", style="Addfds.TLabel")
        self.add_twentyfive.bind(
            "<Button-1>", lambda event, x=25: self.add_funds(event, x))

        self.add_fifty = ttk.Label(
            self.fr_add_fifty, text="50,--€ Guthaben aufladen", style="Addfds.TLabel")
        self.add_fifty.bind("<Button-1>", lambda event,
                            x=50: self.add_funds(event, x))

        self.add_hundred = ttk.Label(
            self.fr_add_hundred, text="100,--€ Guthaben aufladen", style="Addfds.TLabel")
        self.add_hundred.bind("<Button-1>", lambda event,
                              x=100: self.add_funds(event, x))

        self.fr_balance_big = Frame(master=self.funds_frame, bg=act_dark)
        self.balance_big = ttk.Label(self.fr_balance_big, text="Aktuelles Guthaben", style="TB.TLabel",
                                     background=act_dark)

        self.balance_value_label = ttk.Label(self.fr_balance_big, text=str(self.get_balance()) + "€", style="TB.TLabel",
                                             background=act_dark)
        self.balance_value_label.configure(font=("arial", 12))

        # ====================================== SHOP PAGE ======================================

        self.shop_page = Frame(master=self.mainframe, bg=pas_dark)
        self.shop_page.columnconfigure(0, weight=7)
        self.shop_page.columnconfigure(1, weight=3)
        self.shop_page.rowconfigure(0, weight=1)
        self.shop_page.rowconfigure(1, weight=29)

        self.sorting_bar_sh = Frame(master=self.shop_page, bg=pas_dark)

        # TODO: Scrollable mit mousewheel machen
        self.game_listings_frame = ScrollableFrame(container=self.shop_page)

        # for i, game in enumerate(self.all_games):
        for game in self.all_games:
            temp_frame = GameFrame(
                container=self.game_listings_frame.scrollable_frame, game=game)
            self.game_frames.append(temp_frame)
            temp_frame.grid(column=0, sticky="news")
            # if game in self.shop_games:
            #     self.game_frames[i].grid()

        self.cart = Frame(master=self.shop_page, bg="blue")

        self.sort_by_price_label = ttk.Label(self.sorting_bar_sh, text="Sortieren nach Preis", width=20,
                                             style="Sorting.TLabel")
        self.sort_by_price_label.bind("<Button-1>", self.sort_by_price)

        self.sort_shop_by_name_label = ttk.Label(self.sorting_bar_sh, text="Sortieren nach Name", width=20,
                                                 style="Sorting.TLabel")
        self.sort_shop_by_name_label.bind("<Button-1>", self.sort_shop_by_name)

        self.open_shop(event=None)  # Show the shop on launch

    def open_shop(self, event):
        if self.showing != "shop":
            self.shop_label.configure(font=("arial", 20, "bold"))
            self.lib_label.configure(font=('arial', 20))

            self.lib_page.grid_forget()
            self.funds_frame.grid_forget()

            self.shop_page.grid(row=1, column=0, sticky="wens")

            self.sorting_bar_sh.grid(row=0, column=0, sticky="wens")

            self.game_listings_frame.grid(
                row=1, column=0, sticky='nsew', padx=20, pady=20)

            self.cart.grid(row=1, column=1, sticky="wens")

            self.sort_by_price_label.grid(row=0, column=1, sticky="w")

            self.sort_shop_by_name_label.grid(row=0, column=1, sticky="w")

            for game_frame in self.game_frames:
                if game_frame.game in self.shop_games:
                    game_frame.grid()
                else:
                    game_frame.grid_forget()

            self.showing = "shop"

    def open_lib(self, event):
        self.shop_page.grid_forget()
        self.funds_frame.grid_forget()
        self.lib_label.configure(font=("arial", 20, "bold"))
        self.shop_label.configure(font=('arial', 20))

        self.lib_page.grid(row=1, column=0, sticky="wens")

        self.sorting_bar_lib.grid(row=0, column=0, sticky="wens")

        self.info_tab.grid(row=1, column=1, sticky="wens")

        self.sort_by_playtime_label.grid(row=0, column=1, sticky="w")

        self.sort_lib_by_name_label.grid(row=0, column=1, sticky="w")

        self.game_library_frame.grid(
            row=1, column=0, sticky='nsew', padx=20, pady=20)

        for game_frame in self.game_frames:
            if game_frame.game in self.lib_games:
                # game_frame.container = # TODO: Man kann container nicht im Nachhinein ändern, deshalb müssen alle
                #  GameFrames auf beiden Seiten erstellt werden aber wie z.B.
                # wenn ein Game rausgenommen wird und neue Reihenfolge dort ist? Ordnen sie sich neu?
                # TODO: CSGO wird nicht in LIB angezeigt
                game_frame.grid()
            else:
                game_frame.grid_forget()

        self.showing = "lib"

        # print("Opening library")

    def open_funds(self, event):
        self.shop_page.grid_forget()
        self.lib_page.grid_forget()
        self.shop_label.configure(font=('arial', 20))
        self.lib_label.configure(font=('arial', 20))
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

        self.fr_balance_big.grid(
            row=0, column=1, sticky="wens", padx=10, pady=10)
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
        self.balance = round(self.balance + amount, 2)
        # print("Guthaben müsste {},--€ aufgeladen werden".format(amount))
        new_amount_str = str(self.balance) + "€"
        self.balance_value_label["text"] = new_amount_str
        self.balance_label["text"] = new_amount_str

    def get_balance(self):
        # balance = 1.60384572
        self.balance = round(self.balance, 2)
        return '{:.2f}'.format(self.balance)

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
        print("Nach Spielzeit sortieren")
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
        self.canvas = tk.Canvas(self, bg="purple")
        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg=act_dark)
        # self.canvas.columnconfigure(0, weight=1)
        # self.canvas.rowconfigure(0, weight=1)
        # self.scrollable_frame.columnconfigure(0, weight=1)
        # self.scrollable_frame.rowconfigure(0, weight=1)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                # Wird aufgerufen wenn sich Inhalte ändern --> scrollregion wird
                scrollregion=self.canvas.bbox("all")
                # aktualisiert
            )
        )

        self.canvas_frame = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind('<Configure>', self.frame_width)

    def frame_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


def game_str(platforms):
    ret = ""
    for platform in platforms:
        ret += platform + ", "
    ret = ret[:-2]
    return ret


class GameFrame(ttk.Frame):
    def __init__(self, container, game, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.game = game

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.game_frame = Frame(master=container, bg=act_dark)

        self.game_frame.columnconfigure(0, weight=1)  # Image
        self.game_frame.columnconfigure(1, weight=1)  # Name, Platforms, Genre
        self.game_frame.columnconfigure(2, weight=1)  # Discount tag if needed
        # Add/remove to/from cart Button
        self.game_frame.columnconfigure(3, weight=1)

        self.game_frame.rowconfigure(0, weight=1)  # Name
        self.game_frame.rowconfigure(1, weight=1)  # Platforms
        self.game_frame.rowconfigure(2, weight=1)  # Genre

        self.img = ttk.Label(self.game_frame, image=game.img, background=pas_dark)
        self.img.grid(row=0, column=0, rowspan=3, sticky="w")

        self.l_name = ttk.Label(
            self.game_frame, text=game.name, style="GameDesc.TLabel", background=act_dark)
        self.l_name.grid(row=0, column=1, sticky="w")

        self.l_platforms = ttk.Label(self.game_frame, text=game_str(game.platforms), style="GameDesc.TLabel",
                                     background=act_dark)
        self.l_platforms.grid(row=1, column=1, sticky="w")

        self.l_genre = ttk.Label(self.game_frame, text=game_str(
            game.genre), style="GameDesc.TLabel", background=act_dark)
        self.l_genre.grid(row=2, column=1, sticky="w")

        if game.discounted:
            self.l_discounted = ttk.Label(
                self.game_frame, text="%", style="TB.TLabel", background=act_dark)
            self.l_discounted.grid(row=1, column=2, padx=10, pady=10)

        add_to_cart_icon = ImageTk.PhotoImage(Image.open("imgs/addcart.png"))
        remove_from_cart_icon = ImageTk.PhotoImage(
            Image.open("imgs/rmcart.png"))
        if game.in_cart:
            self.cart_icon = Label(
                self.game_frame, image=remove_from_cart_icon, bg=act_dark)
            self.cart_icon.bind("<Button-1>", game.remove_from_cart)
            self.cart_icon.image = remove_from_cart_icon

        else:
            self.cart_icon = Label(self.game_frame, image=add_to_cart_icon, bg=act_dark)
            self.cart_icon.bind("<Button-1>", game.to_cart)
            self.cart_icon.image = add_to_cart_icon

        self.cart_icon.grid(row=0, column=3, rowspan=3,
                            padx=10, pady=10, sticky="nsew")

        self.game_frame.grid(column=0, sticky="nsew", padx=10, pady=10)


def main():
    # root = Tk()
    root = ThemedTk()
    style = ttk.Style()
    style.theme_use('clam')
    # print(style.theme_names())
    # style.configure("C.TButton", foreground="white", background="black", relief="groove")
    # style.configure("TButton", foreground="green", background="black")
    style.configure("TB.TLabel", foreground="white",
                    background=pas_dark, anchor="center", font=('arial', 20))
    style.configure(root, background=pas_dark, foreground="white")
    style.configure("Sorting.TLabel", font=("arial", 12),
                    background=pas_dark, anchor="center")
    style.configure("FundsAmount.TLabel", font=(
        'arial', 14), background=act_dark)
    style.configure("GameDesc.TLabel", font=('arial', 12))
    dampf = Dampf(root, style)  # , get_balance())
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
