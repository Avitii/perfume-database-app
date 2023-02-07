import cv2
import sqlite3
import pyzbar.pyzbar as bar
import os
import time
from rich.console import Console
from rich.table import Table
# all above is needed, some additional functionality to basic python


def menu():
    # firstly ask user to select file and decode EAN from photo
    barcode = init()

    # print menu and wait for choice
    while True:
        show_menu(barcode)
        print()
        sel = input("Wpisz numer opcji z listy: ")
        info = db_info(barcode)

        if sel == "1":
            option_add(barcode, info)
        elif sel == "2":
            option_remove(barcode)
        elif sel == "3":
            option_info(barcode, info)
        elif sel == "4":
            menu()
        else:
            cli_clear()
            print("Wybrana opcja nie istnieje!")
            print()
            input("Naciśnij Enter aby wrócić do Menu..")


def init():
    while True:
        # show files found in images dir
        path = "images/"
        show_files(os.listdir(path))
        print()

        # ask for file name
        file = input("Wpisz pełną nazwę pliku z listy: ")

        # check if file is in images dir, if not, return to file choose menu
        if file not in os.listdir(path):
            cli_clear()
            print("Nie znaleziono pliku o tej nazwie!")
            print()
            input("Naciśnij Enter aby spróbować ponownie..")
        else:
            decoded = str(barcode_read(path + file))
            decoded = decoded.replace("b", "")
            decoded = decoded.replace("'", "", 2)
            return decoded


def db_info(barcode):
    # establish connection to db
    conn = sqlite3.connect('database.sqlite')
    db = conn.cursor()

    db.execute("""SELECT * FROM perfume WHERE barcode = ?""",
               (barcode,))

    # return results found in database
    return db.fetchall()


# function for file show handling
def show_files(files):
    cli_clear()

    # of course show files as table
    table = Table(title="[Dostępne pliki]")
    columns = ["     Nazwa     "]

    for column in columns:
        table.add_column(column)

    for n in files:
        table.add_row(n)

    Console().print(table)


def show_menu(barcode):
    cli_clear()

    table = Table(title="[EAN: " + barcode + "]")
    rows = [["1", "Dodaj do bazy"],
            ["2", "Usuń z bazy"],
            ["3", "Wyświetl informacje"],
            ["4", "Wybór pliku"]]
    columns = ["Opcja", "Opis"]

    for column in columns:
        table.add_column(column)

    for row in rows:
        table.add_row(*row)

    Console().print(table)


def option_add(barcode, info):
    # check if list is empty or if barcode is already added
    if not info:
        option_add_final(barcode)
    elif barcode in info[0]:
        cli_clear()
        print("Ten produkt znajduje się już w bazie!")
        print()
        input("Naciśnij Enter aby wrócić do Menu..")
    else:
        option_add_final(barcode)


def option_add_final(barcode):
    cli_clear()

    # collect needed informations
    brand = input("Wpisz markę: ")
    name = input("Wpisz nazwę: ")
    type = input("Wpisz typ: ")
    group = input("Wpisz grupę zapachów: ")
    head = input("Wpisz nuty głowy: ")
    heart = input("Wpisz nuty serca: ")
    base = input("Wpisz nuty podstawy: ")

    # establish connection to db
    conn = sqlite3.connect('database.sqlite')
    db = conn.cursor()

    # add row to table perfume with provided values
    db.execute("""INSERT INTO perfume VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
               (barcode, brand, name, type, group, head, heart, base))

    # save changes and close connection to db
    conn.commit()
    conn.close()

    print()
    print("Dane zapisane.")
    time.sleep(2)


def option_remove(barcode):
    # to be shure info
    cli_clear()
    print("Czy na pewno chcesz usunąć produkt o kodzie " + barcode + " z bazy danych?")
    confirm = input("Wpisz TAK aby potwierdzić lub NIE aby wrócić do Menu: ")

    if confirm == "TAK":
        # establish connection to db
        conn = sqlite3.connect('database.sqlite')
        db = conn.cursor()

        # delete row from table perfume where barcode equals readed barcode
        db.execute("""DELETE FROM perfume WHERE barcode = ?""",
                   (barcode,))

        # save changes and close connection to db
        conn.commit()
        conn.close()

        print()
        print("Usunięto produkt z bazy.")
        time.sleep(2)
    else:
        print()
        print("Usuwanie produktu anulowane.")
        time.sleep(2)


def option_info(barcode, info):
    cli_clear()

    # no info found
    if not info:
        print("Nie znaleziono informacji o tym produkcie!")
        print()
        input("Naciśnij Enter aby wrócić do Menu..")
    # print found info as nice table :D
    else:
        table = Table(title="[EAN: " + barcode + "]")
        rows = [[info[0][1], info[0][2], info[0][3], info[0][4], info[0][5], info[0][6], info[0][7], ]]
        columns = ["Marka", "Nazwa", "Typ", "Grupa zapachów", "Głowa", "Serce", "Podstawa"]

        for column in columns:
            table.add_column(column)

        for row in rows:
            table.add_row(*row)

        Console().print(table)
        print()
        input("Naciśnij Enter aby wrócić do Menu..")


def barcode_read(image):
    # load image
    img = cv2.imread(image)

    # decode barcode
    dbarcode = bar.decode(img)

    # no ean message
    if not dbarcode:
        cli_clear()
        print("Nie wykryto kodu EAN!")
        print()
        input("Naciśnij Enter aby wybrać inny plik..")
        menu()
    else:
        for barcode in dbarcode:
            return barcode.data


# function to clear console
def cli_clear():
    # check os
    if os.name == "posix":
        # linux
        os.system("clear")
    else:
        # windows
        os.system("cls")


if __name__ == '__main__':
    menu()
