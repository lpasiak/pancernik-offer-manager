def context_menu():
    menu_text = """--------------------------------
Z czym dziś chcesz pracować?
0. Eksportować produkty
1. Rozprawić się z outletami
2. Menedżer promocji
3. Menedżer zestawów
4. Shopify
5. IdoSell
6. Allegro
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_export():
    menu_text = """--------------------------------
Skąd chcesz pobrać dane?
1. Shoper
2. Shopify Light
3. Shopify Bizon
4. EasyStorage Pancernik
5. EasyStorage Bizon
6. IdoSell
7. Shoper | Beautiful products
all. Wszystko powyżej
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_outlet():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. Wystawić outlety
2. Obniżki na outlety
3. Usunąć stare przekierowania
4. Przenieść sprzedane/archiwalne
5. Atrybuty produktów
all. Wszystko powyżej
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_promo():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. Usunąć promocje
2. Zaimportować promocje procentowe i stany
3. Zaimportować promocje stałe dla Kuby
4. Zaimportować promocje zgodne z AlleObniżki dla Maćka
5. Eksportować promocje
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_bundle():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. MaxExport zdjęć
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_shopify():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. Podmienić URL-e/tytuły/opis z pliku CSV (sheets/handles-bizon.csv)
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_idosell():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. Dograć produktom ceny ostatniej dostawy, wagi i wymiary
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_allegro():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. Test
q żeby wyjść.
Akcja: """
    return str(input(menu_text))
