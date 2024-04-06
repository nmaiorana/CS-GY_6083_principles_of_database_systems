# Test db_utils.py
import unittest

import mysql
import pandas as pd

import tools.db_utils as dbu


class DBUtilsTest(unittest.TestCase):
    def test_get_connector(self):
        with dbu.get_connector() as conn:
            self.assertIsNotNone(conn)
            self.assertIsInstance(conn, mysql.connector.connection_cext.CMySQLConnection)

    def test_query_to_df(self):
        df = dbu.query_to_df("SELECT * FROM record_albums")
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)



