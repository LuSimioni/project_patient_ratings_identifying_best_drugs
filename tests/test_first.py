import unittest
import pandas as pd
import os
from io import StringIO
from unittest.mock import patch, mock_open
import json
from src.utils import load_csv_to_dataframe, camel_to_snake, rename_columns, set_column_types, extrair_do_sql, load_settings, decode_dataframe, create_index_column

class TestFunctions(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='col1,col2\n1,2\n3,4')
    def test_load_csv_to_dataframe(self, mock_file):
        df = load_csv_to_dataframe('dummy_path.csv')
        self.assertEqual(df.shape, (2, 2))
        self.assertListEqual(df.columns.tolist(), ['col1', 'col2'])

    def test_decode_dataframe(self):
        data = {'col1': ['café', 'naïve']}
        df = pd.DataFrame(data)
        df = decode_dataframe(df)
        self.assertEqual(df['col1'].iloc[0], 'café')
        self.assertEqual(df['col1'].iloc[1], 'naïve')

    @patch.dict(os.environ, {
        "POSTGRES_HOST": "localhost",
        "POSTGRES_USER": "user",
        "POSTGRES_PASSWORD": "password",
        "POSTGRES_DB": "db",
        "POSTGRES_PORT": "5432"
    })
    def test_load_settings(self):
        settings = load_settings()
        self.assertEqual(settings['db_host'], 'localhost')
        self.assertEqual(settings['db_user'], 'user')
        self.assertEqual(settings['db_pass'], 'password')
        self.assertEqual(settings['db_name'], 'db')
        self.assertEqual(settings['db_port'], '5432')

    @patch('pandas.read_sql')
    @patch('sqlalchemy.create_engine')
    def test_extrair_do_sql(self, mock_create_engine, mock_read_sql):
        mock_engine = mock_create_engine.return_value
        mock_conn = mock_engine.connect.return_value.__enter__.return_value
        mock_read_sql.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        query = "SELECT * FROM table"
        df = extrair_do_sql(query)
        self.assertEqual(df.shape, (2, 2))
        self.assertListEqual(df.columns.tolist(), ['col1', 'col2'])

    @patch('builtins.open', new_callable=mock_open, read_data='{"col1": "int", "col2": "float"}')
    def test_set_column_types(self, mock_file):
        data = {'col1': ['1', '2'], 'col2': ['3.0', '4.0']}
        df = pd.DataFrame(data)
        df = set_column_types(df, 'dummy_path.json')
        self.assertEqual(df['col1'].dtype, 'int')
        self.assertEqual(df['col2'].dtype, 'float64')

    def test_camel_to_snake(self):
        self.assertEqual(camel_to_snake('camelCase'), 'camel_case')
        self.assertEqual(camel_to_snake('PascalCase'), 'pascal_case')

    def test_create_index_column(self):
        data = {'col1': [1, 2]}
        df = pd.DataFrame(data)
        df = create_index_column(df)
        self.assertEqual(df.columns.tolist()[0], 'id')
        self.assertEqual(df['id'].iloc[0], 1)

    def test_rename_columns(self):
        data = {'camelCase': [1, 2], 'PascalCase': [3, 4], 'unnamed: 0': [5, 6]}
        df = pd.DataFrame(data)
        df = rename_columns(df)
        self.assertListEqual(df.columns.tolist(), ['id', 'camel_case', 'pascal_case'])
        self.assertEqual(df['id'].iloc[0], 1)

if __name__ == '__main__':
    unittest.main()