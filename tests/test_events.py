#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/25/18

import unittest
from evenz.events import Event, event, observable


@observable
class TestClass1(object):
    __test__ = False

    @event
    def event1(self, s: str):
        """
        Describe what the event does.

        :param s: gimme a string
        """


class TestSuite(unittest.TestCase):

    def test_extend_subscribe_count(self):
        print('\n' * 3)
        tc1 = TestClass1()
        #self.assertTrue(True)
        x = tc1.event1
        tc1.event1 += lambda s: print(s)
        tc1.event1 += lambda s: print(len(s))

        tc1.event1('blahhh!!!')
        tc1.event1('bork!!!')

        def another(s: str):
            print(f"I am another {s}!")
        tc1.event1 += another

        tc1.event1('omigorsh')
        tc1.event1 -= another
        tc1.event1('alacadala')




if __name__ == '__main__':
    unittest.main()

