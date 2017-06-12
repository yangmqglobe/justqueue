# -*- coding:utf-8 -*-
#
# author: yangmqglobe
# file: exceptions.py
# time: 2017/6/11


class JustQueueError(Exception):
    """
    all Exception raised by justqueue is extend by this exception
    """
    pass


class UnsupportedTypeError(JustQueueError):
    """
    raise when pushing an unsupported item into the queue
    """
    pass


class EmptyQueueError(JustQueueError):
    """
    raise when getting item from an empty queue
    """
    pass


class QueueClosedError(JustQueueError):
    """
    raise when operate the queue after close(call the close() function) it
    """
    pass
