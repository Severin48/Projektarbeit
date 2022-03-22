import tkinter as tk
from tkinter import ttk
from tkinter import *
from ttkthemes import ThemedTk
from PIL import ImageTk, Image

width = 1200  # 900, 720
height = 700  # 600, 512
small = height / 20

act_dark = "#2d384b"
pas_dark = "#1f232a"

# TODO: Typing

dampf = None


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
    style.configure("GameName.TLabel", background=pas_dark,
                    anchor="center", font=('arial', 12, "bold"))
    style.configure("GameDesc.TLabel", background=pas_dark,
                    anchor="center", font=('arial', 10))
    style.configure("PriceTag.TLabel", font=('arial', 12))
    style.configure("LibInfo.TLabel", font=("arial", 14),
                    background=pas_dark, anchor="center")

    global dampf
    dampf = Dampf(root, style)
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


def add_to_cart(event, game):
    # print("Adding to cart: ", game.handle)
    game.in_cart = True
    gf = game.shop_game_frame
    gf.cart_icon.configure(image=gf.remove_from_cart_icon)
    gf.cart_icon.image = gf.remove_from_cart_icon

    gf.cart_icon.bind("<Button-1>", lambda e,
                      g=game: remove_from_cart(e, g))

    dampf.refresh_shop()


def remove_from_cart(event, game):
    # print("Removing from cart: ", game.handle)
    game.in_cart = False
    gf = game.shop_game_frame
    gf.cart_icon.configure(image=gf.add_to_cart_icon)
    gf.cart_icon.image = gf.add_to_cart_icon

    gf.cart_icon.bind("<Button-1>", lambda e,
                      g=game: add_to_cart(e, g))

    dampf.refresh_shop()


def get_total_playtime_str():
    if dampf is None:
        return "Keine"
    else:
        total_playtime = 0
        for game in dampf.all_games:
            if game.owned:
                total_playtime += game.playtime
        return time_to_str(total_playtime)


def time_to_str(playtime):
    h = playtime // 3600
    # TODO hier Fabians Methode mit Modulo nehmen
    mn = round(((playtime / 3600) - h) * 60)
    sec = round(((((playtime / 3600) - h) * 60) - mn) * 60)
    # TODO: Fabian hat noch Tage dazu gemacht.
    #  Aber bei steam eig nicht

    return str(h) + "h " + str(mn) + "m " + str(sec) + "s"


def get_total_value_str():
    if dampf is None:
        return "Keine"
    else:
        total_value = 0
        for game in dampf.all_games:
            if game.owned:
                total_value += game.price
        return str(total_value) + "€"


def refund(event, g):
    if g.playtime > 3600*2:  # 2h
        # TODO: Popup refund nicht möglich weil mehr als 2h Spielzeit
        pass
    else:
        print("Returning")
        g.owned = False
        dampf.balance += g.price
        dampf.refresh_shop()
        dampf.refresh_lib()


def sort_frames(page, by):
    if page == "shop":
        del dampf.shop_items
        dampf.shop_items = []
        shop_games = []
        for sg in dampf.all_games:
            if not sg.owned:
                shop_games.append(sg)
        if by == "name":
            # 1. Sort Frames 2. Loop through sorted list and put onto grid - sorted list comes from students
            ret = sorted(shop_games, key=lambda g: g.name)
        elif by == "price":
            ret = sorted(shop_games, key=lambda g: g.price)
        dampf.shop_items = ret.copy()
        dampf.refresh_shop()
    elif page == "lib":
        lib_games = []
        for lg in dampf.all_games:
            if lg.owned:
                lib_games.append(lg)
        if by == "name":
            ret = sorted(lib_games, key=lambda g: g.name)
        elif by == "playtime":
            ret = sorted(lib_games, key=lambda g: g.playtime)
        dampf.refresh_lib(ret)
    else:
        return -1


class Game:
    # TODO: Doc welche Einheiten/Typen z.B. Playtime in Sekunden
    def __init__(self, name, genre, platforms, img, handle, owned=False, discounted=False, price=0, playtime=0):
        self.name = name
        self.price = price
        self.genre = genre
        self.platforms = platforms
        self.discounted = discounted
        self.playtime = playtime
        self.in_cart = False
        self.owned = owned
        self.img = ImageTk.PhotoImage(Image.open("imgs/" + img + ".png"))
        self.img_play = ImageTk.PhotoImage(
            Image.open("imgs/" + img + "_play" + ".png"))
        self.handle = handle
        self.shop_game_frame = None
        self.lib_game_frame = None

    def __repr__(self):
        return "Game_" + self.name


# TODO: Wenn genug Funds vorhanden sind nicht auf AddFundsPage


class Dampf:
    def __init__(self, master, style):  # , balance):
        self.master = master
        self.style = style
        self.balance = 0  # alt: = balance
        master.title("Dampf")
        self.showing = ""
        self.all_games = []
        self.shop_game_frames = []
        self.lib_game_frames = []
        self.shop_items = []

        self.all_games.append(Game("Ruf der Pflicht:\nModerne Kriegskunst 2", ["First-person shooter", "Action"],
                                   ["Windows"], img="mw2", discounted=True, handle="MW2", price=19.99, playtime=0))

        self.all_games.append(Game("Gegenschlag:\nGlobale Offensive", ["Action", "Free to play"],
                                   ["Windows", "Linux", "Mac"], img="cs",
                                   handle="CSGO", playtime=101882))

        self.all_games.append(Game("Die Älteren Rollen:\nHimmelsrand", ["RPG", "Fantasy"],
                                   ["Windows", "Linux"], img="tes5", discounted=True,
                                   handle="TES V", price=39.99, playtime=48920))

        self.all_games.append(Game("Gothisch 2:\nDie Nacht des Raben", ["RPG", "Fantasy"],
                                   ["Windows", "Linux"], img="g2", handle="G2: DndR", price=9.99, playtime=48920))

        self.all_games.append(Game("Zeitalter der Imperien III", ["Strategie"],
                                   ["Windows"], img="aoe", handle="AoE III", price=19.99, playtime=48920, owned=True))

        self.mainframe = Frame(master=self.master, bg=pas_dark)
        self.mainframe.rowconfigure(0, weight=1)  # Top bar
        self.mainframe.rowconfigure(1, weight=29)  # Shop Listing & Cart
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.grid(row=0, column=0, sticky="WENS")

        self.top_bar = Frame(master=self.mainframe, bg=pas_dark)
        self.top_bar.columnconfigure(0, weight=2)
        self.top_bar.columnconfigure(1, weight=2)
        self.top_bar.columnconfigure(2, weight=14)
        self.top_bar.columnconfigure(3, weight=1)
        self.top_bar.columnconfigure(4, weight=1)
        self.top_bar.rowconfigure(0, weight=1)
        self.top_bar.grid(row=0, column=0, sticky="WENS")
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
        balance_str = str(self.get_balance()) + "€"
        self.balance_label = ttk.Label(
            self.fr_balance_label, text=balance_str)
        self.balance_label.grid(row=0, column=0, sticky="E", padx=5, pady=5)
        self.balance_label.bind("<Button-1>", self.open_funds)

        # ====================================== LIB PAGE ======================================

        self.lib_page = Frame(master=self.mainframe, bg=pas_dark)
        self.lib_page.columnconfigure(0, weight=8)
        self.lib_page.columnconfigure(1, weight=2)
        self.lib_page.rowconfigure(0, weight=1)
        self.lib_page.rowconfigure(1, weight=29)

        self.sorting_bar_lib = Frame(master=self.lib_page, bg=pas_dark)

        self.info_tab = Frame(master=self.lib_page, bg=act_dark)

        self.info_tab.rowconfigure(0, weight=1)
        self.info_tab.rowconfigure(1, weight=1)
        self.info_tab.rowconfigure(2, weight=8)
        self.info_tab.columnconfigure(0, weight=1)

        self.sort_by_playtime_label = ttk.Label(self.sorting_bar_lib, text="Sortieren nach Spielzeit", width=20,
                                                style="Sorting.TLabel")
        self.sort_by_playtime_label.bind("<Button-1>", self.sort_by_playtime)

        self.sort_lib_by_name_label = ttk.Label(self.sorting_bar_lib, text="Sortieren nach Name", width=20,
                                                style="Sorting.TLabel")
        self.sort_lib_by_name_label.bind("<Button-1>", self.sort_lib_by_name)

        self.game_library_frame = ScrollableFrame(container=self.lib_page)

        for game in self.all_games:
            temp_frame = LibGameFrame(
                container=self.game_library_frame.scrollable_frame, game=game)
            self.lib_game_frames.append(temp_frame)

        self.l_total_value = ttk.Label(
            self.info_tab, text="Gesamtwert: 0€", style="LibInfo.TLabel")

        self.l_total_playtime = ttk.Label(self.info_tab, text="Gesamtspielzeit: 0 h 0 min 0 sec",
                                          style="LibInfo.TLabel")

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
        self.shop_page.columnconfigure(0, weight=8)  # Main section
        self.shop_page.columnconfigure(1, weight=2)  # Cart section
        self.shop_page.rowconfigure(0, weight=1)
        self.shop_page.rowconfigure(1, weight=29)

        self.sorting_bar_sh = Frame(master=self.shop_page, bg=pas_dark)

        # TODO: Scrollable mit mousewheel machen
        self.game_listings_frame = ScrollableFrame(container=self.shop_page)

        for game in self.all_games:
            temp_frame = ShopGameFrame(
                container=self.game_listings_frame.scrollable_frame, game=game)
            self.shop_game_frames.append(temp_frame)

        self.sort_by_price_label = ttk.Label(self.sorting_bar_sh, text="Sortieren nach Preis", width=20,
                                             style="Sorting.TLabel")
        self.sort_by_price_label.bind("<Button-1>", self.sort_by_price)

        self.sort_shop_by_name_label = ttk.Label(self.sorting_bar_sh, text="Sortieren nach Name", width=20,
                                                 style="Sorting.TLabel")
        self.sort_shop_by_name_label.bind("<Button-1>", self.sort_shop_by_name)

        # =================== Cart section ===================

        self.fr_cart = Frame(master=self.shop_page, bg=act_dark)

        self.fr_cart.columnconfigure(0, weight=1)
        self.fr_cart.rowconfigure(0, weight=1)

        self.cart_desc = ttk.Label(self.fr_cart, text="In ihrem Warenkorb befinden sich\nfolgende Spiele:",
                                   background=act_dark, width=38)

        self.cart_labels = []
        self.cart_delete_labels = []
        for i in range(10):
            self.cart_labels.append(ttk.Label(
                self.fr_cart, text="No Game", background=act_dark, foreground=act_dark))
            self.fr_cart.rowconfigure(i + 1, weight=1)
            self.cart_delete_labels.append(ttk.Label(self.fr_cart,
                                                     text="Löschen", background=pas_dark))

        price_str = str(self.get_total_cart_price()) + "€"
        self.l_total_sum = ttk.Label(
            self.fr_cart, text=price_str, background=pas_dark)

        self.l_clear_cart = ttk.Label(
            self.fr_cart, text="Warenkorb löschen", background=pas_dark)
        self.l_clear_cart.bind("<Button-1>", self.clear_cart)

        self.l_buy_cart = ttk.Label(
            self.fr_cart, text="Kaufen", background="green")
        self.l_buy_cart.bind("<Button-1>", self.buy_cart)

        # https://stackoverflow.com/questions/29091747/set-tkinter-label-texts-as-elements-of-list
        # TODO: Oder eine feste Menge (8) Labels, deren Texte nach einer Liste an Games im cart geändert werden.
        #  Wenn mehr als 8 Spiele im Cart sind, werden zwei Buttons sichtbar, mit denen man die Seiten browsen kann.
        #  Oder einfach leicht machen und mehr als genug Labels machen und nur manche davon befüllen.

        self.open_shop(event=None)  # Show the shop on launch

    def get_total_cart_price(self):
        price_sum = 0
        for g in self.all_games:
            if g.in_cart:
                price_sum += g.price
        return round(price_sum, 2)

    def clear_cart(self, event):
        for g in self.all_games:
            if g.in_cart:
                g.in_cart = False
                remove_from_cart(None, g)
        self.refresh_shop()

    def buy_cart(self, event):
        price_sum = self.get_total_cart_price()
        if self.balance >= price_sum:
            for g in self.all_games:
                if g.in_cart:
                    g.in_cart = False
                    remove_from_cart(None, g)
                    g.owned = True
            self.balance -= price_sum
            self.refresh_shop()
        else:
            self.open_funds(event)

    def refresh_shop(self, sorted_sg=None):
        # shop_games = []
        cart_games = []
        # if not sorted_sg:
        for game in self.all_games:
            if game.in_cart:
                cart_games.append(game)
        #         if not game.owned:
        #             shop_games.append(game)
        # else:
        #     shop_games = sorted_sg  # .copy()
        #     cart_games = []
        #     for game in self.all_games:
        #         if game.in_cart:
        #             cart_games.append(game)

        for game_frame in self.shop_game_frames:
            game_frame.grid_forget()
        for sg in self.shop_items:
            sg.shop_game_frame.grid()

        for cl in self.cart_labels:
            cl.grid_forget()
        for cdl in self.cart_delete_labels:
            cdl.grid_forget()

        for i, game in enumerate(cart_games):
            self.cart_labels[i].grid(column=0, row=i + 1)
            self.cart_labels[i].configure(
                text=game.name, foreground="white", background=act_dark)
            self.cart_delete_labels[i].grid(column=1, row=i + 1, sticky="e")
            self.cart_delete_labels[i].bind("<Button-1>", lambda e, g=game,
                                            gf=game.shop_game_frame: remove_from_cart(e, g))

        if len(cart_games) == 0:
            self.cart_desc.configure(
                text="Ihr Warenkorb ist leer.", anchor="center")
            self.l_total_sum.grid_forget()
            self.l_buy_cart.grid_forget()
            self.l_clear_cart.grid_forget()
        else:
            self.cart_desc.configure(
                text="In ihrem Warenkorb befinden sich\nfolgende Spiele:")
            self.l_total_sum.grid(row=len(cart_games)+1,
                                  column=0, columnspan=2)
            cart_sum_str = "Gesamtpreis: " + \
                str(self.get_total_cart_price()) + "€"
            self.l_total_sum.configure(text=cart_sum_str)
            self.l_buy_cart.grid(row=len(cart_games)+2, column=0)
            self.l_clear_cart.grid(row=len(cart_games)+2, column=1)

        balance_str = str(self.get_balance()) + "€"
        self.balance_label.config(text=balance_str)

    def open_shop(self, event):
        del self.shop_items
        self.shop_items = []
        for g in self.all_games:
            if not g.owned and not g.in_cart:
                self.shop_items.append(g)

        self.shop_label.configure(font=("arial", 20, "bold"))
        self.lib_label.configure(font=('arial', 20))

        self.lib_page.grid_forget()
        self.funds_frame.grid_forget()

        self.shop_page.grid(row=1, column=0, sticky="wens")

        self.sorting_bar_sh.grid(
            row=0, column=0, sticky="wens", columnspan=2)

        self.game_listings_frame.grid(
            row=1, column=0, sticky='nsew', padx=20, pady=20)

        self.sort_by_price_label.grid(row=0, column=1, sticky="w")

        self.sort_shop_by_name_label.grid(row=0, column=1, sticky="w")

        self.fr_cart.grid(row=1, column=1, sticky="wens")

        self.cart_desc.grid(column=0, row=0, columnspan=2)

        self.refresh_shop()

        self.showing = "shop"

    def refresh_lib(self, sorted_lg=None):
        lib_games = []
        if not sorted_lg:
            for game in self.all_games:
                if game.owned:
                    lib_games.append(game)
        else:
            lib_games = sorted_lg  # .copy()

        for game_frame in self.lib_game_frames:
            game_frame.grid_forget()
        for lg in lib_games:
            lg.lib_game_frame.grid()

        self.l_total_value.configure(
            text="Gesamtwert: " + get_total_value_str())
        self.l_total_playtime.configure(
            text="Gesamtspielzeit: " + get_total_playtime_str())

    def open_lib(self, event):
        self.shop_page.grid_forget()
        self.funds_frame.grid_forget()
        self.lib_label.configure(font=("arial", 20, "bold"))
        self.shop_label.configure(font=('arial', 20))

        self.lib_page.grid(row=1, column=0, sticky="wens")

        self.sorting_bar_lib.grid(row=0, column=0, sticky="wens", columnspan=2)

        self.info_tab.grid(row=1, column=1, sticky="wens")

        self.sort_by_playtime_label.grid(row=0, column=1, sticky="w")

        self.sort_lib_by_name_label.grid(row=0, column=1, sticky="w")

        self.l_total_value.grid(row=0, column=0)

        self.l_total_playtime.grid(row=1, column=0)

        self.game_library_frame.grid(
            row=1, column=0, sticky='nsew', padx=20, pady=20)

        self.refresh_lib()

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
        sort_frames("shop", "price")
        self.sort_by_price_label.grid_forget()
        self.sort_shop_by_name_label.grid()

    def sort_shop_by_name(self, event):
        # TODO: Hier gute Fehlermeldungen printen je nach Wert den man zurückbekommt oder je nach Error
        print("Nach Name Sortieren")
        sort_frames("shop", "name")
        self.sort_shop_by_name_label.grid_forget()
        self.sort_by_price_label.grid()

    def sort_lib_by_name(self, event):
        # TODO: Hier gute Fehlermeldungen printen je nach Wert den man zurückbekommt oder je nach Error
        print("Nach Name Sortieren")
        sort_frames("lib", "name")
        self.sort_lib_by_name_label.grid_forget()
        self.sort_by_playtime_label.grid()

    def sort_by_playtime(self, event):
        print("Nach Spielzeit sortieren")
        sort_frames("lib", "playtime")
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
        self.canvas = tk.Canvas(self, bg=act_dark)
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


class ShopGameFrame(ttk.Frame):
    def __init__(self, container, game, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.game = game
        game.shop_game_frame = self

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        self.game_frame = Frame(master=container, bg=act_dark)

        self.game_frame.columnconfigure(0, weight=1)  # Image
        self.game_frame.columnconfigure(1, weight=1)  # Name, Platforms, Genre
        self.game_frame.columnconfigure(2, weight=1)  # Discount tag if needed
        # Add/remove to/from cart Button
        self.game_frame.columnconfigure(3, weight=1)

        self.game_frame.rowconfigure(0, weight=1)  # Name
        self.game_frame.rowconfigure(1, weight=1)  # Platforms
        self.game_frame.rowconfigure(2, weight=1)  # Genre

        self.img = ttk.Label(
            self.game_frame, image=game.img, background=act_dark)

        self.l_name = ttk.Label(
            self.game_frame, text=game.name, style="GameName.TLabel", anchor="w", background=act_dark)

        self.l_platforms = ttk.Label(self.game_frame, text=game_str(game.platforms), style="GameDesc.TLabel",
                                     background=act_dark, anchor="w")

        self.l_genre = ttk.Label(self.game_frame, text=game_str(
            game.genre), style="GameDesc.TLabel", background=act_dark, anchor="w")

        self.l_discounted = ttk.Label(
            self.game_frame, text="%", style="TB.TLabel", background=act_dark, anchor="center")

        self.add_to_cart_icon = ImageTk.PhotoImage(
            Image.open("imgs/addcart.png"))
        self.remove_from_cart_icon = ImageTk.PhotoImage(
            Image.open("imgs/rmcart.png"))

        self.cart_icon = Label(self.game_frame, bg=act_dark)

        if game.price == 0:
            price_str = "Free to play"
        else:
            price_str = str(game.price) + "€"
        self.price_tag = ttk.Label(
            self.game_frame, text=price_str, style="PriceTag.TLabel", background=act_dark, foreground="white")

    def __repr__(self):
        return "GameFrame_" + self.game.name

    def grid(self):
        self.img.grid(row=0, column=0, rowspan=3, sticky="w")
        self.l_name.grid(row=0, column=1, sticky="w")
        self.l_platforms.grid(row=1, column=1, sticky="w")
        self.l_genre.grid(row=2, column=1, sticky="w")

        if self.game.discounted:
            self.l_discounted.configure(foreground="green")
        else:
            self.l_discounted.configure(foreground=act_dark)

        self.l_discounted.grid(row=1, column=2)

        if self.game.in_cart:
            self.cart_icon.configure(image=self.remove_from_cart_icon)
            self.cart_icon.bind("<Button-1>", lambda event,
                                g=self.game: remove_from_cart(event, g))
            self.cart_icon.image = self.remove_from_cart_icon
        else:
            self.cart_icon.configure(image=self.add_to_cart_icon)
            self.cart_icon.bind("<Button-1>", lambda event,
                                g=self.game: add_to_cart(event, g))
            self.cart_icon.image = self.add_to_cart_icon

        self.cart_icon.grid(row=1, column=3, rowspan=2, sticky="nsew")
        self.price_tag.grid(row=0, column=3)
        self.game_frame.grid(column=0, sticky="nsew")

    def grid_forget(self):
        self.img.grid_forget()
        self.l_name.grid_forget()
        self.l_platforms.grid_forget()
        self.l_genre.grid_forget()
        self.l_discounted.grid_forget()
        self.cart_icon.grid_forget()
        self.price_tag.grid_forget()
        self.game_frame.grid_forget()


class LibGameFrame(ttk.Frame):
    def __init__(self, container, game, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.game = game
        game.lib_game_frame = self

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.game_frame = Frame(master=container, bg=act_dark)

        self.game_frame.columnconfigure(0, weight=1)  # Image
        self.game_frame.columnconfigure(1, weight=1)  # Name, Platforms, Genre
        self.game_frame.columnconfigure(2, weight=1)  # Space buffer
        # Playtime info and refund button
        self.game_frame.columnconfigure(3, weight=1)

        self.game_frame.rowconfigure(0, weight=1)  # Name
        self.game_frame.rowconfigure(1, weight=1)  # Platforms
        self.game_frame.rowconfigure(2, weight=1)  # Genre

        self.img = ttk.Label(
            self.game_frame, image=game.img_play, background=act_dark)

        self.l_name = ttk.Label(
            self.game_frame, text=game.name, style="GameName.TLabel", anchor="w", background=act_dark)

        self.l_platforms = ttk.Label(self.game_frame, text=game_str(game.platforms), style="GameDesc.TLabel",
                                     background=act_dark, anchor="w")

        self.l_genre = ttk.Label(self.game_frame, text=game_str(
            game.genre), style="GameDesc.TLabel", background=act_dark, anchor="w")

        playtime_str = time_to_str(game.playtime)
        self.l_playtime = ttk.Label(self.game_frame, text=playtime_str, style="GameDesc.TLabel",
                                    background=act_dark, anchor="w")

        self.l_refund = ttk.Label(self.game_frame, text="Zurückgeben", style="GameDesc.TLabel",
                                  background=act_dark, anchor="w")
        self.l_refund.bind("<Button-1>", lambda event,
                           g=self.game: refund(event, g))

        self.game_frame.grid(column=0, sticky="nsew")

    def __repr__(self):
        return "GameFrame_" + self.game.name

    def grid(self):
        self.img.grid(row=0, column=0, rowspan=3, sticky="w")
        self.l_name.grid(row=0, column=1, sticky="w")
        self.l_platforms.grid(row=1, column=1, sticky="w")
        self.l_genre.grid(row=2, column=1, sticky="w")

        self.l_playtime.grid(row=0, column=3, sticky="w")
        self.l_refund.grid(row=1, column=3, sticky="w")

        self.game_frame.grid(column=0, sticky="nsew")

    def grid_forget(self):
        self.img.grid_forget()
        self.l_name.grid_forget()
        self.l_platforms.grid_forget()
        self.l_genre.grid_forget()
        self.l_playtime.grid_forget()
        self.l_refund.grid_forget()
        self.game_frame.grid_forget()


if __name__ == '__main__':
    main()
