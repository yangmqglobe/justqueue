# -*- coding:utf-8 -*-
#
# author: yangmqglobe
# file: fifoqueue.py
# time: 2017/6/11
from .utils import tran_item, reduce_item
from .utils import not_closed
from .exceptions import EmptyQueueError
import os
import sqlite3


class FIFOQueue(object):
    _sql_create = """CREATE TABLE IF NOT EXISTS "fifoqueue"
                      ("id" INTEGER PRIMARY KEY AUTOINCREMENT , "item" TEXT, "type" TEXT)"""
    _sql_push = 'INSERT INTO "fifoqueue" ("item", "type") VALUES (?, ?)'
    _sql_len = 'SELECT COUNT("id") FROM "fifoqueue"'
    _sql_get = 'SELECT "item", "type" FROM "fifoqueue" ORDER BY "id" LIMIT ?'
    _sql_del = 'DELETE FROM "fifoqueue" WHERE "id" IN (SELECT "id" FROM "fifoqueue" ORDER BY "id" LIMIT ?)'

    def __init__(self, path, items=None, overwrite=False):
        """
        init the queue
        :param path: the path you want to store the sqlite db file
        :param items: push some items when init the queue, iterable
        :param overwrite: overwrite the queue db file if it has exist?
        """
        self.path = os.path.abspath(path)
        if overwrite and os.path.exists(self.path):
            os.remove(self.path)
        self.conn = sqlite3.connect(self.path)
        with self.conn as conn:
            conn.execute(self._sql_create)
            if items:
                conn.executemany(self._sql_push, (tran_item(item) for item in items))

    @not_closed
    def __len__(self):
        """
        get the size of this queue
        :return: size of this queue
        """
        with self.conn as conn:
            size, = conn.execute(self._sql_len).fetchone()
            return size

    @not_closed
    def close(self, remove=True):
        """
        close the connection with the db
        :param remove: if this queue is empty, delete it?
        """
        size = len(self)
        self.conn.close()
        if size == 0 and remove:
            os.remove(self.path)

    @not_closed
    def peek(self):
        """
        get the first item in this queue but would not delete it
        :return: the first item in this queue
        """
        with self.conn as conn:
            try:
                value, type_ = conn.execute(self._sql_get, (1,)).fetchone()
            except TypeError:
                raise EmptyQueueError('Peek an empty queue')
            return reduce_item(value, type_)

    @not_closed
    def peeks(self, num):
        """
        generate the items which are locate at the beginning of this queue but would not delete them
        :param num: how many items do you want?
        :return: items which are locate at the beginning of this queue(generator)
        """
        with self.conn as conn:
            for value, type_ in conn.execute(self._sql_get, (num,)).fetchall():
                yield reduce_item(value, type_)

    @not_closed
    def pop(self):
        """
        get the first item in this queue and delete it
        :return: the first item in this queue
        """
        with self.conn as conn:
            try:
                value, type_ = conn.execute(self._sql_get, (1,)).fetchone()
            except TypeError:
                raise EmptyQueueError('Pop from an empty queue')
            conn.execute(self._sql_del, (1,))
            return reduce_item(value, type_)

    @not_closed
    def pops(self, num):
        """
        generate the items which are locate at the beginning of this queue and delete them
        :param num: how many items you want?
        :return: items which are locate at the beginning of this queue(generator)
        """
        with self.conn as conn:
            for value, type_ in conn.execute(self._sql_get, (num,)).fetchall():
                yield reduce_item(value, type_)
                conn.execute(self._sql_del, (1,))
