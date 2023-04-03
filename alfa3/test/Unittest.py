import unittest
from unittest.mock import patch
import sqlalchemy as exc
from main import import_csv_data, import_xml_data, insert_order, delete_record, connection, update_record, \
    make_transaction


class TestImportCSVData(unittest.TestCase):

    @patch('connect.execute')
    def test_import_csv_data(self, mock_execute):
        file_path = 'test.csv'
        table_name = 'test'

        import_csv_data(file_path, table_name)

        expected = f"""LOAD DATA INFILE '{file_path}' INTO TABLE {table_name}
        FIELDS TERMINATED BY ',' 
        ENCLOSED BY '"' 
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS;"""

        mock_execute.assert_called_with(expected)






class TestImportXMLData(unittest.TestCase):

    @patch('xml.etree.ElementTree.parse')
    def test_import_xml_data(self, mock_parse):
        file_path = 'test_file.xml'
        table_name = 'test_table'

        # Mock the XML data to be parsed
        mock_data = [{'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}]

        # Set up the mock parse method to return the mock data
        mock_parse.return_value = mock_data

        # Call the import XML data function with the mocked data
        result = import_xml_data(file_path, table_name)

        # Assert that the result is as expected
        self.assertEqual(result, {'field1': 'value1', 'field2': 'value2', 'field3': 'value3'})






class TestMakeTransaction(unittest.TestCase):

    @patch('connection.begin')
    def test_make_transaction_success(self, mock_begin):
        order_data = {'customer_id': 1, 'order_date': '2020-01-01'}
        order_items_data = [{'product_id': 1, 'quantity': 2}, {'product_id': 2, 'quantity': 3}]

        make_transaction(order_data, order_items_data)

        mock_begin.assert_called()

    @patch('connection.begin')
    def test_make_transaction_failure(self, mock_begin, order__data=None, mock__begin=None):
        order_data = {'customer__id': 1, 'order__date': '2020-01-01'} # Invalid data

        with self.assertRaises(Exception):
            make_transaction(order__data)

            mock__begin.assert__not__called()




class TestDatabaseMethods(unittest.TestCase):

    def setUp(self):
        self.order_data = {'customer_id': 1, 'order_date': '2020-01-01', 'items': [{'product_id': 2, 'quantity': 3}, {'product_id': 4, 'quantity': 5}]}

    def test_insert_order(self):
        order_id = insert_order(self.order_data)
        self.assertIsNotNone(order_id)

    def test_delete_record(self):
        delete_record('orders', 1)
        result = connection.execute("SELECT * FROM orders WHERE id=1").fetchone()
        self.assertIsNone(result)

    def test_update_record(self):
        update_record('orders', 1, 'customer_id', 2)
        result = connection.execute("SELECT * FROM orders WHERE id=1").fetchone()[1]
        self.assertEqual(result, 2)

    def tearDown(self, transaction=None):
        # Zrušení transakce při chybě v testu
        try:
            transaction.rollback()
        except exc.SQLAlchemyError as e:
            raise e