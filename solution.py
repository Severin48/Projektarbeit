# TODO: Kommentare und erwartete Ergebnisse aufschreiben + Leere Lösung
def add_to_balance(old_balance, amount):
    return old_balance + amount


def add_game_to_cart(games_in_cart, game_to_add):
    return games_in_cart.append(game_to_add) # TODO: ?


def remove_game_from_cart(games_in_cart, game_to_remove):
    return games_in_cart.remove(game_to_remove)


def calculate_price_with_discount(game_price, discounted):
    if discounted:
        if game_price < 20:
            actual_price = game_price * 0.9
        elif game_price <= 50:
            actual_price = game_price * 0.75
        elif game_price > 50:
            actual_price = game_price * 0.5

    return round(actual_price, 2)


def calculate_total_cart_price(prices):
    total_sum = 0
    for price in prices:
        total_sum += price
    return round(total_sum, 2)


def enough_balance(cart_price, account_balance):
    return cart_price <= account_balance


def pay(cart_price, account_balance):
    return account_balance - cart_price


def playtime_from_seconds(seconds):
    h = round(seconds / 3600)
    secs_left = seconds % 3600
    # TODO: Studenten warnen, dass "min" eine eingebaute Funktion ist und kein geeigneter Variablenname.
    m = round(secs_left / 60)
    s = secs_left % 60

    return h, m, s


def total_library_value(prices):
    total_value = 0
    for price in prices:
        total_value += price
    return round(total_value, 2)


if __name__ == 'main':
    pass


