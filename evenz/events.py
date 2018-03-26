#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/25/18
"""
.. currentmodule:: events
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Say something descriptive about the 'events' module.
"""

import inspect
from typing import Any, Callable, Iterable, List, NamedTuple, Tuple
from functools import wraps


class Args(NamedTuple):
    """
    Extend this named tuple to provide easy-to-understand arguments for your events.
    """
    sender: Any  #: the originator of the event


class Event(object):
    """
    Use events to be notified when a something happens.

    .. seealso::

        While you can instantiate an instance of this class directly, check out the
        :py:func:`event` decorator first.
    """
    def __init__(self, f: Callable):
        # Each instance needs to have its own class so that we can specify __call__ (which is
        # only searched on the class).
        self.__class__ = type(self.__class__.__name__, (self.__class__,), {})
        self.__class__.__call__ = self.__trigger__
        # Keep a reference to the original function.
        self._f = f
        # Create a list to hold the handlers.
        self._handlers = []

    @property
    def function(self) -> Callable:
        """
        Get the original function from which the event was created.

        :return: the original function
        """
        return self._f

    @property
    def handlers(self) -> Iterable[Callable]:
        """
        Get the handlers for this function.

        :return: an iteration of the handlers.
        """
        return iter(self._handlers)

    def subscribe(self, handler: Callable):
        """
        Subscribe a handler function to this event.

        :param handler: the handler

        .. note::

            You can also use the += operator.
        """
        self._handlers.append(handler)

    def unsubscribe(self, handler: Callable):
        """
        Unsubscribe a handler function from this event.

        :param handler: the handler

        .. note::

            You can also use the -= operator.
        """
        self._handlers.remove(handler)

    def __iadd__(self, other):
        # Sanity check:  The 'other' parameter should be a handler function.
        if not isinstance(other, Callable):
            raise ValueError(f'{type(other)} is not callable.')
        # Append handler.
        self._handlers.append(other)
        return self

    def __isub__(self, other):
        # Remove the handler.
        self._handlers.remove(other)
        return self

    def __and__(self, other):
        a = set(self._handlers)
        b = set(other)
        ab = a & b
        self._handlers = [h for h in self._handlers if h in ab]
        return self

    def __or__(self, other):
        a = set(self._handlers)
        b = set(other)
        ab = a | b
        self._handlers = [h for h in self._handlers if h in ab]
        return self

    def __trigger__(self, *args, **kwargs):
        # Just call all the handlers.
        for h in self._handlers:
            h(*args, **kwargs)


def observable(cls):
    """
    Use this decorator to mark a class that exposes events.

    :param cls: the class
    :return: the class

    .. seealso::

        If you are using this decorator, you probably also want to use :py:func:`event` on
        some of the methods.
    """
    # For starters, we need the class' original __init__ method.
    cls_init = cls.__init__

    # THIS IS WHERE TO START...
    cls_events: List[Tuple[str, Event]] = [
        cls_event for cls_event in inspect.getmembers(cls)
        if isinstance(cls_event[1], Event)
    ]
    for cls_event in cls_events:

        name, event_ = cls_event

        def f(*args, **kwargs) -> Event:
            return event_

        setattr(f, '__doc__', event_.function.__doc__)
        setattr(f, '__event_method__', True)
        setattr(cls, name, f)

        #event_prop = property(lambda self: event, None, None, event_.function.__doc__)
        #setattr(cls, name, event_prop)
        #event_.function.__event_method__ = True
        #setattr(cls, name, event_.function)




    @wraps(cls.__init__)
    def init(self, *args, **kwargs):
        # Call the class' original __init__ method.
        cls_init(self, *args, **kwargs)
        self.__class__ = type(self.__class__.__name__, (self.__class__,), {})
        # Retrieve all the methods marked as events.
        event_members_: List[Tuple[str, Event]] = [
            member for member in inspect.getmembers(self)
            #if isinstance(member[1], Event)
            if hasattr(member[1], '__event_method__')
            and member[1].__event_method__
        ]
        for event_member_ in event_members_:
            name_, event_method = event_member_
            #e = Event(event_method)
            e = Event(event_method())
            setattr(self, name_, e)

    # Replace the class' original __init__ method with our own.
    cls.__init__ = init
    # The caller gets back the original class.
    return cls


def event(f: Callable) -> Event:
    """
    Decorate a function or method to create an :py:class:`Event`.

    :param f: the function.
    :return: the event

    .. seealso::

        If you are decorating a method within a class, you'll need to use the
        :py:func:`observable` class decorator on the class as well.
    """
    # Create an event for the callable.
    e = Event(f)
    # That should be all we need to do.
    return e


@observable
class Dog(object):
    """
    This is a dog that can bark.  We can also listen for a 'barked' event.

    """

    def __init__(self, name: str):
        """
        Give the dog a name.
        :param name:
        """
        self.name = name  #: this is the dog name

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

    @property
    def blah(self):
        "here is what I do"
        return 1