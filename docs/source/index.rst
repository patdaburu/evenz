.. evenz documentation master file
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

evenz
=====

Simplify event-driven python!

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   api
   development
   requirements

Introduction
============

Overview
--------

`evenz` is a simplified implementation of the
`observer pattern <https://en.wikipedia.org/wiki/Observer_pattern>`_ in python.  It uses some
friendly syntax conventions from other languages.

Create a Class with Events
---------------------------

For this simple example we'll create an observable object with just one event.

.. code-block:: python

    from evenz import observable, event

    @observable
    class Dog(object):
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

Handle Events
-------------

Now let's respond to the observable object's event by subscribing handler methods.

.. code-block:: python

    # Create our observable dog.
    dog = Dog()

    # Create a handler function for the dog's 'barked' event.
    def on_bark(sender: Dog, count: int):
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



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
