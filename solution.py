def set_username():
    """
    Setzt den Benutzernamen in der Top-Bar.
    :return: String, der den Namen enthält.
    """
    return "Student"  # Hier den Namen einfüllen


def add_to_balance(old_balance, amount):
    """
    Hier wird das vorhandene Guthaben (old_balance) um den Betrag (amount) aufgeladen. Das ergebnis soll auf zwei
    Nachkommastellen gerundet werden.
    In allen folgenden Methoden ist das Runden auf zwei Nachkommastellen wichtig, da ansonsten ein floating point error
    für viele Nachkommastellen sorgen kann, welche als Geldbetrag keinen Sinn machen.
    Die Seite, auf der man das Guthaben aufladen kann erscheint, wenn man zu wenig Guthaben für den Kauf hat oder beim
    Klicken auf den Betrag oben rechts.
    :param old_balance: Vorhandenes (altes) Guthaben.
    :param amount: Betrag, der aufgeladen wird.
    :return: Gerundeter Gesamtbetrag.
    """
    return round(old_balance + amount, 2)


def add_game_to_cart(games_in_cart, game_to_add):
    """
    Ein Spiel (game_to_add) soll den Spielen, die sich bereits im Warenkorb befinden (games_in_cart), hinzugefügt
    werden.
    :param games_in_cart: Liste von Spielen, die bereits im Warenkorb sind.
    :param game_to_add: Spiel, das hinzugefügt werden soll.
    :return: Eine Liste, welche sowohl die alten als auch das neu hinzugefügt Spiel beinhaltet.
    """
    games_in_cart.append(game_to_add)
    return games_in_cart


def remove_game_from_cart(games_in_cart, game_to_remove):
    """
    Aus der Liste der Spiele im Warenkorb (games_in_cart) soll ein Spiel (game_to_remove) entfernt werden.
    :param games_in_cart: Liste von Spielen, die bereits im Warenkorb sind.
    :param game_to_remove: Spiel, das entfernt werden soll.
    :return: Eine Liste, welche abgesehen vom Spiel (game_to_remove) die selben Elemente beinhalten soll.
    """
    games_in_cart.remove(game_to_remove)
    return games_in_cart


def calculate_price_with_discount(game_price, discounted):
    """
    Für Spiele, welche rabattiert sind (discounted = True), soll aus dem alten Preis (game_price) der neue Preis
    berechnet werden.
    Für bestimmte Preisklassen gibt es fixe Rabattprozentzahlen.
    Auf Spiele, die unter 20€ kosten gibt es 10% Rabatt, unter 50€ 25% Rabatt und Spiele ab 50€ kosten die Hälfte.
    :param game_price: Voller Spielpreis in Euro (float).
    :param discounted: Bool, welcher angibt, ob Rabatt auf ein Spiel gerechnet werden muss. discounted = True heißt
    auf das Spiel gibt es Rabatt.
    :return: Der neue und eventuell verringerte Preis in Euro als float und auf zwei Nachkommastellen gerundet.
    """
    if discounted:
        if game_price < 20:
            actual_price = game_price * 0.9
        elif game_price < 50:
            actual_price = game_price * 0.75
        else:  # == elif game_price > 50:
            actual_price = game_price * 0.5
        return round(actual_price, 2)
    else:
        return game_price


def calculate_total_cart_price(prices):
    """
    Der Gesamtwert des Warenkorbs soll durch die einzelnen Preise der im Warenkorb befindlichen Spiele errechnet werden.
    :param prices: Liste mit Preisen der einzelnen Spiele.
    :return: Gesamtpreis als float auf zwei Nachkommastellen gerundet.
    """
    total_sum = 0
    for price in prices:
        total_sum += price
    return round(total_sum, 2)


def enough_balance(cart_price, account_balance):
    """
    Diese Funktion soll prüfen, ob genug Guthaben (account_balance) auf dem Konto ist, um die Inhalte des Warenkorbs mit
    Gesamtpreis cart_price zu kaufen. Zurückgegeben werden soll ein Wahrheitswert (bool), ob das Geld ausreicht.
    :param cart_price: Gesamtpreis der Spiele im Warenkorb als float.
    :param account_balance: Guthaben, das zur Verfügung steht als float.
    :return: Bool, ob das Guthaben ausreicht um die Spiele zu kaufen.
    """
    return cart_price <= account_balance


def pay(cart_price, account_balance):
    """
    In dieser Funktion wird der Warenkorb bezahlt. Dazu werden der Gesamtpreis (cart_price) und das Guthaben
    (account_balance) in der Berechnung verwendet. Es soll das Guthaben berechnet werden, das nach dem Kauf übrig
    bleibt.
    :param cart_price: Gesamtwert der Spiele im Warenkorb.
    :param account_balance: Guthaben, das zur Verfügung steht.
    :return: Auf zwei Nachkommastellen gerundetes, übrig gebliebenes Guthaben nach dem Kauf.
    """
    return round(account_balance - cart_price, 2)


def playtime_from_seconds(seconds):
    """
    Die Spielzeit wird in Sekunden übergeben (seconds) und muss in Stunden, Minuten und Sekunden umgerechnet werden.
    Hierbei lässt es sich nicht empfehlen die Minutenvariable "min" zu nennen, da dies ein eingebauter Name in Python
    ist.
    Tipp: Eine Stunde hat 3600 Sekunden und Modulorechnung (%-Operator) ist nützlich. Alternativ kann man auch die
    Ganzzahldivision (//-Operator) verwenden.
    :param seconds: Spielzeit in Sekunden als int.
    :return: Dreiertupel oder Liste der Form h, m, s (Stunden, Minuten, Sekunden) - in einem return-Statement. Hierbei
    sollen alle Werte des Typs int sein also keine Nachkommastellen haben.
    """
    h = round(seconds / 3600)
    secs_left = seconds % 3600
    m = round(secs_left / 60)
    s = secs_left % 60

    return [h, m, s]


def total_library_value(prices):
    """
    Es soll der Gesamtwert der besessenen Spiele berechnet werden.
    :param prices: Eine Liste der einzelnen Preise.
    :return: Ein auf zwei Nachkommastellen gerundeter Gesamtwert aller Spiele im Besitz des Nutzers.
    """
    total_value = 0
    for price in prices:
        total_value += price
    return round(total_value, 2)


if __name__ == 'main':
    # TODO: Zum Ausführen dampf.py starten. Für Hinweise auf die Konsolenausgaben achten.
    #  Falls diese Datei (z.B. zum Testen) ausgeführt werden soll, muss der Code hierher geschrieben werden. Falls Code
    #  außerhalb dieses if-statements steht (abgesehen von Klassen-/Methoden-/Funktionendeklarationen), wird er auch
    #  beim Importieren der Datei (und damit beim Starten von dampf.py) ausgeführt.
    pass
