# This file is placed in the Public Domain.


"handler"


## import

import unittest


from op import Handler


## class


class TestHandler(unittest.TestCase):

    def testconstructor(self):
        hdl = Handler()
        self.assertEqual(type(hdl), Handler)
