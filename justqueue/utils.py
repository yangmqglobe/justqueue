# -*- coding:utf-8 -*-
#
# author: yangmqglobe
# file: utils.py
# time: 2017/6/12
from functools import wraps
from sqlite3 import ProgrammingError
from .exceptions import UnsupportedTypeError
from .exceptions import QueueClosedError

# functions use to tran the item to str to store in db
_tran_item = {
    int: lambda item: (str(item), 'int'),
    float: lambda item: (str(item), 'float'),
    str: lambda item: (item, 'str')
}

# functions use to reduce the item to it's original type
_reduce_item = {
    'int': lambda value: int(value),
    'float': lambda value: float(value),
    'str': lambda value: value
}


def tran_item(item):
    """
    transform an item to str
    :param item: input item
    :return: str of the item and it's original type
    """
    try:
        return _tran_item[type(item)](item)
    except KeyError:
        raise UnsupportedTypeError('type {} is not supported'.format(type(item)))


def reduce_item(value, type_):
    """
    reduce the item to it's original type
    :param value: item's str
    :param type_: item's original type
    :return:
    """
    return _reduce_item[type_](value)


def not_closed(func):
    """
    decorate a function that can call before close the queue
    :param func: a function
    :return: a new function has been decorate
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ProgrammingError:
            raise QueueClosedError('This queue has been closed')
    return wrapper

