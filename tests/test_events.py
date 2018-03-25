#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/25/18

import unittest
from evenz.events import observable, event

@observable
class Dog(object):
    __test__ = False
    """
    This is a dog that can bark.  We can also listen for a 'barked' event.

    """
    def bark(self, count: int):
        """
        Call this method to make the dog bark.

        :param count: How many times will the dog bark?
        """
        for i in range(0, count):
            print('Woof!')
        self.barked(count)

    @event
    def barked(self, count: int):
        """
        This event is raised when the dog barks.

        :param count: how many times did the dog bark?
        """


class TestSuite(unittest.TestCase):
    def test_arrange_act_assert(self):
        # Create our observable dog.
        dog = Dog()

        # Create a handler function for the dog's 'barked' event.
        def on_bark(count: int):
            for i in range(0, count):
                print('Hush, puppy!')

        # When the dog barks, we'll respond.
        dog.barked += on_bark

        # Have the dog bark a few times.
        dog.bark(5)

        # At this point, we're fed up and no longer listening for barks.
        dog.barked -= on_bark

        # Now the dog's barks should go without a response.
        print('OK.  We are no longer listening.')
        dog.bark(5)


if __name__ == '__main__':
    unittest.main()

