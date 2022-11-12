# This file is placed in the Public Domain.


"event"


## import


import unittest


from op import Event


## class


class TestEvent(unittest.TestCase):

    def testconstructor(self):
        evt = Event()
        self.assertEqual(type(evt), Event)
