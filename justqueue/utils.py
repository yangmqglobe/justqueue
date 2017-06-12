# -*- coding:utf-8 -*-
#
# author: yangmqglobe
# file: utils.py
# time: 2017/6/12
from .exceptions import UnsupportedTypeError

_tran_item = {
    int: lambda item: (str(item), 'int'),
    float: lambda item: (str(item), 'float'),
    str: lambda item: (item, 'str')
}


def tran_item(item):
    try:
        return _tran_item[type(item)](item)
    except KeyError:
        raise UnsupportedTypeError('type {} is not supported'.format(type(item)))
