# This file is placed in the Public Domain.


"database"


## import


import unittest


from op import Db


## class


class TestDbs(unittest.TestCase):

    def test_constructor(self):
        dbs = Db()
        self.assertEqual(type(dbs), Db)
