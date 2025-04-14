def context_menu():
    menu_text = """--------------------------------
Z czym dziś chcesz pracować?
0. Pobrać informacje o produktach
1. Menedżer outletów
2. Menedżer promocji
3. Menedżer zestawów
4. Podmiana Shopify
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_outlet():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. Wystawić outlety
2. Obniżki na outlety
3. Przenieść sprzedane/archiwalne
4. Atrybuty produktów
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_promo():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. Pobrać promocje
2. Zaimportować promocje
3. Uaktualnić stany magazynowe
4. Usunąć promocje
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_bundle():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. Utworzyć zestaw
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
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_shopify():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. Podmienić URL-e z pliku CSV (sheets/handles-bizon.csv)
q żeby wyjść.
Akcja: """
    return str(input(menu_text))
