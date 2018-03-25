#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/25/18
"""
.. currentmodule:: events
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Say something descriptive about the 'events' module.
"""

import inspect
from typing import Any, Callable, Iterable, List, Tuple
from functools import wraps








class Event(object):

    def __init__(self, f: Callable):
        self._f = f

        _call = self.__call__
        @wraps(f)
        def call(*args, **kwargs):
            _call(*args, **kwargs)
        self.__call__ = call


        # wrap the original function for this object's __call__ method
        self._handlers = []

    @property
    def function(self) -> Callable:
        return self._f

    @property
    def handlers(self) -> Iterable[Callable]:
        return iter(self._handlers)

    def subscribe(self, handler: Callable):
        self._handlers.append(handler)

    def unsubscribe(self, handler: Callable):
        self._handlers.remove(handler)

    def __iadd__(self, other):
        self._handlers.append(other)
        return self

    def __isub__(self, other):
        self._handlers.remove(other)
        return self

    def __call__(self, *args, **kwargs):
        for h in self._handlers:
            h(*args, **kwargs)


def observable(cls):
    # For starters, we need the class' original __init__ method.
    cls_init = cls.__init__

    @wraps(cls.__init__)
    def init(self, *args, **kwargs):
        # Call the class' original __init__ method.
        cls_init(self, *args, **kwargs)
        # Retrieve all the methods marked as events.
        event_members: List[Tuple[str, Event]] = [
            member for member in inspect.getmembers(self)
            if isinstance(member[1], Event)
        ]
        for event_member in event_members:
            e = Event(event_member[1].function)
            self.__dict__[event_member[0]] = e
    # Replace the class' original __init__ method with our own.
    cls.__init__ = init
    # The caller gets back the original class.
    return cls


def event(f: Callable):
    # Create an event for the callable.
    e = Event(f)

    # wrap the event's call method around the function!

    # TODO: Copy docstring!
    return e
