import configparser
from mysql.connector import connect
from sqlalchemy import create_engine, exc
import xml.etree.ElementTree as ET




"""
Tento kód vytváří motor pro připojení k databázi. Používá modul configparser k načtení konfiguračního souboru (config.ini) a poté použije hodnoty v sekci 'databáze' konfiguračního souboru k vytvoření objektu engine.
Engine se poté použije k vytvoření objektu připojení, který se vytiskne se zprávou, že připojení bylo úspěšné.
"""
config = configparser.ConfigParser()
config.read('config.ini')

db_config = config['database']


# Vytvoření enginu pro připojení k databázi
engine = create_engine(f'mysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}')

connection = engine.connect()
print("Připojeno.")




# Importováni dat do databáze
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
Tato funkce aktualizuje záznam v dané tabulce.
Vyžaduje čtyři parametry: název_tabulky (řetězec), id záznamu (celé číslo), sloupec (řetězec) a nová_hodnota (řetězec).
Funkce pomocí SQL dotazu aktualizuje daný sloupec novou hodnotou pro zadaný záznam v zadané tabulce.
"""
def import_csv_data(file_path, table_name):

    # Vložení dat
    load_data_query = f"""LOAD DATA INFILE '{file_path}' INTO TABLE {table_name}
    FIELDS TERMINATED BY ',' 
    ENCLOSED BY '"' 
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;"""
    connect.execute(load_data_query)


    connection.commit()


"""
Tento kód slouží k importu dat XML do tabulky. Nejprve se pomocí knihovny ET (ElementTree) načte XML soubor ze zadané cesty (filepath). Poté se projde každý element v kořenovém elementu a vloží se do tabulky s názvem tablename.
Data jsou uložena ve třech polích field1, field2 a field3. Nakonec je provedena commit() operace, aby byla data uložena do databáze.
"""
def import_xml_data(file_path, table_name):
    tree = ET.parse(file_path)
    root = tree.getroot()


    # Vložení dat
    for child in root:
        connection.execute(f"INSERT INTO {table_name} (field1, field2, field3) VALUES (%s, %s, %s)", (child.attrib['field1'], child.attrib['field2'], child.attrib['field3']))


    connection.commit()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------







"""
maketransaction() je funkce, která vytváří transakci pro vložení dat do dvou tabulek, objednávek a položek objednávky. Funkce přebírá dva parametry, order_data a order_items_data.
Zahájí transakci pomocí connection.begin(), poté vloží data z orderdata do tabulky objednávek pomocí connection.execute().
Poté získá ID vložené objednávky pomocí connection.execute("SELECT last_insert_rowid()").scalar() a vloží data z order_items_data do tabulky order_items pomocí cyklu for.
Pokud se nevyskytnou žádné chyby, potvrdí transakci pomocí transaktion.commit(), v opačném případě vrátí transakci pomocí transaktion.rollback() a vyvolá chybu.
"""

def make_transaction(order_data, order_items_data):
    transaction = connection.begin()
    try:
        # Vložení dat do tabulky orders

        connection.execute("INSERT INTO orders (customer_id, order_date) VALUES (:customer_id, :order_date)", customer_id=order_data['customer_id'], order_date=order_data['order_date'])

        # Získání ID vložené objednávky
        order_id = connection.execute("SELECT last_insert_rowid()").scalar()

        # Vložení dat do tabulky order_items
        for item in order_items_data:
            connection.execute(
                f"INSERT INTO order_items (order_id, product_id, quantity) VALUES ({order_id}, {item['product_id']}, {item['quantity']})")

        # Potvrzení transakce
        transaction.commit()

    except:
        # Zrušení transakce
        transaction.rollback()
        raise







"""
Tato funkce vloží objednávku do databáze. Zahájí transakci, vloží objednávku do tabulky "objednávky", získá ID vložené objednávky a poté vloží položky objednávky do tabulky "objednávky_položky".
Poté potvrdí transakci a vrátí ID objednávky. Pokud dojde k chybě, vrátí transakci zpět a vyvolá výjimku.
"""

def insert_order(order_data):
    try:
        # Začátek transakce
        transaction = connection.begin()

        # Vložení objednávky do tabulky "orders"
        connection.execute("INSERT INTO orders (customer_id, order_date) VALUES (:customer_id, :order_date)",
                           customer_id=order_data['customer_id'], order_date=order_data['order_date'])

        # Získání ID vložené objednávky
        result = connection.execute("SELECT LAST_INSERT_ID()").fetchone()
        order_id = result[0]

        # Vložení položek objednávky do tabulky "order_items"
        for item in order_data['items']:
            connection.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (:order_id, :product_id, :quantity)",
                               order_id=order_id, product_id=item['product_id'], quantity=item['quantity'])
        # Potvrzení transakce
        transaction.commit()
        return order_id

    except exc.SQLAlchemyError as e:
        # Zrušení transakce
        transaction.rollback()
        raise e






"""
Tato funkce odstraní záznam z dané tabulky v databázi.
Chce to dva parametry:
název_tabulky (řetězec): název tabulky, ze které se má záznam odstranit
recordid (int): id záznamu, který má být vymazán
Pomocí SQL dotazu smaže záznam z dané tabulky s daným id.
"""
def delete_record(table_name, record_id):
    # Smazání záznamu
    connection.execute(f"DELETE FROM {table_name} WHERE id={record_id}")





"""
Tato funkce aktualizuje záznam v dané tabulce.
Vyžaduje čtyři parametry: název_tabulky (řetězec), id záznamu (celé číslo), sloupec (řetězec) a nová_hodnota (řetězec).
Funkce pomocí SQL dotazu aktualizuje daný sloupec novou hodnotou pro zadaný záznam v zadané tabulce.
"""
def update_record(table_name, record_id, column, new_value):
    # Úprava záznamu
    connection.execute(f"UPDATE {table_name} SET {column}='{new_value}' WHERE id={record_id}")




# Uzavření kurzoru a spojení s databázý
connection.close()
