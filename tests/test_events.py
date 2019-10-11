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

    def __init__(self, name: str):
        self.name = name

    def bark(self, count: int):
        """
        Call this method to make the dog bark.

        :param count: How many times will the dog bark?
        """
        self.barked(count)

    @event
    def barked(self, count: int):
        """
        This event is raised when the dog barks.

        :param count: how many times did the dog bark?
        """


class TestSuite(unittest.TestCase):

    def test_init1sub1_raise_count(self):
        barks = 5
        # Create our observable dog.
        dog = Dog('Fido')

        # we're going to keep count of the number of times the
        bark_count = {'value': 0}

        # Create a handler function for the dog's 'barked' event.
        def on_bark(sender, count: int):
            for i in range(0, count):
                bark_count['value'] += 1

        # When the dog barks, we'll respond.
        dog.barked += on_bark
        # Have the dog bark a few times.
        dog.bark(barks)

        # At this point, we're fed up and no longer listening for barks.
#        dog.barked -= on_bark
        dog.barked -= on_bark
        # Now the dog's barks should go without a response.
        dog.bark(barks)
        self.assertEqual(barks, bark_count['value'])

    def test_subUnsub_raise_count(self):
        barks = 5
        # Create our observable dog.
        dog = Dog('Fido')

        # we're going to keep count of the number of times the
        bark_count = {'value': 0}

        # Create a handler function for the dog's 'barked' event.
        def on_bark(sender, count: int):
            for i in range(0, count):
                bark_count['value'] += 1

        # When the dog barks, we'll respond.
        dog.barked += on_bark
        # Have the dog bark a few times.
        dog.bark(barks)

        # At this point, we're fed up and no longer listening for barks.
        dog.barked -= on_bark
        # Now the dog's barks should go without a response.
        dog.bark(barks)
        self.assertEqual(barks, bark_count['value'])

    def test_init2sub1_raise_count(self):
        barks = 5
        # Create our observable dog.
        dog1 = Dog('Fido')
        # Create another observable dog.
        dog2 = Dog('Rover')
        # we're going to keep count of the number of times the
        bark_count = {'value': 0}

        # Create a handler function for the dog's 'barked' event.
        def on_bark(sender, count: int):
            for i in range(0, count):
                bark_count['value'] += 1
        # When the first dog barks, we'll respond.  (But not the second dog.)
        dog1.barked += on_bark
        # Have the dogs bark a few times.
        dog1.bark(barks)
        dog2.bark(barks)
        # At this point, we're fed up and no longer listening for barks.
        dog1.barked -= on_bark
        # Now the dog's barks should go without a response.
        dog1.bark(barks)
        self.assertEqual(barks, bark_count['value'])

    def test_init2sub2_raise_count(self):
        barks = 5
        # Create our observable dog.
        dog1 = Dog('Fido')
        # Create another observable dog.
        dog2 = Dog('Rover')
        # we're going to keep count of the number of times the
        bark_count = {'value': 0}

        # Create a handler function for the dog's 'barked' event.
        def on_bark(sender, count: int):
            for i in range(0, count):
                bark_count['value'] += 1
        # When the first dog barks, we'll respond.  (But not the second dog.)
        dog1.barked += on_bark
        dog2.barked += on_bark
        # Have the dogs bark a few times.
        dog1.bark(barks)
        dog2.bark(barks)
        # At this point, we're fed up and no longer listening for barks.
        dog1.barked -= on_bark
        dog2.barked -= on_bark
        # Now the dog's barks should go without a response.
        dog1.bark(barks)
        dog2.bark(barks)
        self.assertEqual(barks * 2, bark_count['value'])


if __name__ == '__main__':
    unittest.main()

