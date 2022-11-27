"""
Tests for Application
"""
import unittest
import pandas as pd
from program import solver

MAX_TIMEOUT = 180

class TestMLOPS(unittest.TestCase):

    def test_solver_creating(self):
        """
        Check solver can save in the right order
        """
        test_data = {
            'customer_id': [1, 1],
            'product_id': [1, 2],
            'timestamp': [
                pd.Timestamp("2021-01-01 12:01:00").timestamp(),
                pd.Timestamp("2021-01-01 12:05:00").timestamp(),
            ]
        }
        df = pd.DataFrame(test_data)
        df = solver(df)

        self.assertEqual(df.loc[0,'customer_id'], 1)
        self.assertEqual(df.loc[0,'product_id'], 1)
        self.assertEqual(df.loc[0,'timestamp'], 1609502460)
        self.assertEqual(df.loc[1,'customer_id'], 1)
        self.assertEqual(df.loc[1,'product_id'], 2)
        self.assertEqual(df.loc[1,'timestamp'], 1609502700)



    def test_solver_more_180(self):
        """
        Check Solver if time between timestamp more than 3 minutes
        """
        test_data = {
            'customer_id': [1, 1, 1],
            'product_id': [1, 2, 3],
            'timestamp': [
                pd.Timestamp("2021-01-01 12:01:00").timestamp(),
                pd.Timestamp("2021-01-01 12:05:00").timestamp(),
                pd.Timestamp("2021-01-01 12:06:00").timestamp(),
            ]
        }
        df = pd.DataFrame(test_data)
        df = solver(df)

        self.assertEqual(df.loc[0,'session'], 1)
        self.assertEqual(df.loc[1,'session'], 2)
        self.assertEqual(df.loc[2,'session'], 2)

    def test_solver_less_180(self):
        """
        Check Solver if time between timestamp less than 3 minutes
        """
        test_data = {
            'customer_id': [1, 1, 1],
            'product_id': [1, 2, 1],
            'timestamp': [
                pd.Timestamp("2021-01-01 12:01:00").timestamp(),
                pd.Timestamp("2021-01-01 12:03:59").timestamp(),
                pd.Timestamp("2021-01-01 12:07:59").timestamp(),
            ]
        }
        df = pd.DataFrame(test_data)
        df = solver(df)

        self.assertEqual(df.loc[0,'session'], 1)
        self.assertEqual(df.loc[1,'session'], 1)
        self.assertEqual(df.loc[2,'session'], 2)

    def test_solver_comples(self):
        """
        Check Solver at complex conditions
        """
        test_data = {
            'customer_id': [1, 1, 2, 2, 3, 3],
            'product_id': [1, 2, 3, 4, 5, 6],
            'timestamp': [
                pd.Timestamp("2021-01-01 12:01:00").timestamp(),
                pd.Timestamp("2021-01-01 12:05:00").timestamp(),
                pd.Timestamp("2021-01-01 12:02:00").timestamp(),
                pd.Timestamp("2021-01-01 12:03:00").timestamp(),
                pd.Timestamp("2021-01-01 12:02:10").timestamp(),
                pd.Timestamp("2021-01-01 12:10:00").timestamp()
            ]
        }
        df = pd.DataFrame(test_data)
        df = solver(df)
        print(df)
        self.assertEqual(df.loc[0,'customer_id'], 1)
        self.assertEqual(df.loc[0,'session'], 1)
        self.assertEqual(df.loc[1,'customer_id'], 2)
        self.assertEqual(df.loc[1,'session'], 1)
        self.assertEqual(df.loc[2,'customer_id'], 3)
        self.assertEqual(df.loc[2,'session'], 1)
        self.assertEqual(df.loc[3,'customer_id'], 2)
        self.assertEqual(df.loc[3,'session'], 1)
        self.assertEqual(df.loc[4,'customer_id'], 1)
        self.assertEqual(df.loc[4,'session'], 2)
        self.assertEqual(df.loc[5,'customer_id'], 3)
        self.assertEqual(df.loc[5,'session'], 2)