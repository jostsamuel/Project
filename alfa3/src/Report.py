import pandas as pd
from main import engine


def generate_summary_report():

    # Agregovaná data z tabulky Orders
    query1 = '''
        SELECT COUNT(*) as total_orders, SUM(total_price) as total_sales
        FROM Orders
    '''
    df1 = pd.read_sql(query1, engine)

    # Agregovaná data z tabulky Customers
    query2 = '''
        SELECT COUNT(*) as total_customers, AVG(age) as average_age
        FROM Customers
    '''
    df2 = pd.read_sql(query2, engine)

    # Agregovaná data z tabulky Products
    query3 = '''
        SELECT COUNT(*) as total_products, SUM(quantity) as total_quantity
        FROM Products
    '''
    df3 = pd.read_sql(query3, engine)

    # Sestavení reportu
    report = pd.concat([df1, df2, df3], axis=1)

    # Přidání hlavičky a patičky
    report.columns = ['Orders', 'Customers', 'Products']
    report.insert(0, 'Report Type', 'Summary', True)
    report.loc['Total'] = report.sum()

    return report



if __name__ == '__main__':

    generate_summary_report()