# -*- coding:utf-8 -*-
#
# author: yangmqglobe
# file: utils.py
# time: 2017/6/12
from functools import wraps
from sqlite3 import ProgrammingError
from .exceptions import UnsupportedTypeError
from .exceptions import QueueClosedError
import json


class RetryItem(object):
    """
    label an item which need to retry
    """
    def __init__(self, item, again):
        self.item = item
        self.again = again

    def tran(self):
        return json.dumps({'item': self.item, 'again': self.again})

# functions use to tran the item to str to store in db
_tran_item = {
    int: lambda item: (str(item), 'int'),
    float: lambda item: (str(item), 'float'),
    str: lambda item: (item, 'str'),
    dict: lambda item: (json.dumps(item), 'dict'),
    list: lambda item: (json.dumps(item), 'list'),
    RetryItem: lambda item: (item.tran(), 'retry')
}

# functions use to reduce the item to it's original type
_reduce_item = {
    'int': lambda value: int(value),
    'float': lambda value: float(value),
    'str': lambda value: value,
    'dict': lambda value: json.loads(value),
    'list': lambda value: json.loads(value),
    'retry': lambda value: json.loads(value)['item']
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
    except TypeError:
        raise UnsupportedTypeError('item {} is not JSON serializable'.format(item))


def reduce_item(value, type_, retry=False, max_try=0):
    """
    reduce the item to it's original type
    :param value: item's str
    :param type_: item's original type
    :param retry: need retry information?
    :param max_try: max retry
    :return: item
    """
    if retry:
        if type_ == 'retry':
            item = json.loads(value)
            return item['item'], item['again']
        else:
            return _reduce_item[type_](value), max_try
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
