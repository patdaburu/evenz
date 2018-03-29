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

    def __init__(self):
        self._handlers: Iterable[Callable] = []

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
        # Sanity check:  The handler parameter should be a handler function.
        if not isinstance(handler, Callable):
            raise ValueError(f'{type(other)} is not callable.')
        self._handlers.append(handler)
        return self

    def unsubscribe(self, handler: Callable):
        """
        Unsubscribe a handler function from this event.

        :param handler: the handler

        .. note::

            You can also use the -= operator.
        """
        self._handlers.remove(handler)
        return self

    def __iadd__(self, other):
        # Subscribe to the handler.
        return self.subscribe(other)

    def __isub__(self, other):
        return self.unsubscribe(other)

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

    def trigger(self, *args, **kwargs):
        """
        Trigger the event.
        """
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

    # # THIS IS WHERE TO START...
    # cls_events: List[Tuple[str, Event]] = [
    #     cls_event for cls_event in inspect.getmembers(cls)
    #     if isinstance(cls_event[1], Event)
    # ]
    # for cls_event in cls_events:
    #
    #     name, event_ = cls_event
    #
    #     # https://docs.python.org/2/library/functions.html#compile
    #     # ⚡ <- prepend doc?
    #     @wraps(event_.function)
    #     def f(*args, **kwargs) -> Event:
    #         return event_
    #
    #     f.__doc__ = f'⚡ :py:class:`evenz.events.Event`\n{f.__doc__}'
    #
    #     #setattr(f, '__doc__', event_.function.__doc__)
    #     setattr(f, '__event_method__', True)
    #     setattr(cls, name, f)

    import types

    @wraps(cls.__init__)
    def init(self, *args, **kwargs):
        # Call the class' original __init__ method.
        cls_init(self, *args, **kwargs)
        # Retrieve all the methods marked as events.
        event_members: List[Tuple[str, Event]] = [
            member for member in inspect.getmembers(self)
            if hasattr(member[1], '__is_event__')
            and member[1].__is_event__
        ]
        for event_member in event_members:
            # Get the attribute name and bound method.
            name_, event_method = event_member
            # Create a new 'event' function from the original function.
            f = event(event_method.__func__.__func__)
            m = types.MethodType(f, self)

            def setattr_(self, name, value):
                if name != 'event':
                    m.__setattr__(name, value)
            m.__dict__['__setattr__'] = setattr_
            # Create a new bound method.
            setattr(self, name_, m)
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
    e = Event()

    @wraps(f)
    def _f(*args, **kwargs):
        e.trigger(*args, **kwargs)

    setattr(_f, 'event', e)
    setattr(_f, 'subscribe', e.subscribe)
    setattr(_f, 'unsubscribe', e.unsubscribe)
    setattr(_f, '__is_event__', True)
    setattr(_f, '__func__', f)

    return _f


