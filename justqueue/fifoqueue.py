# -*- coding:utf-8 -*-
#
# author: yangmqglobe
# file: fifoqueue.py
# time: 2017/6/11
from .utils import tran_item
import os
import sqlite3


class FIFOQueue(object):
    _sql_create = """CREATE TABLE IF NOT EXISTS "justqueue"
                      ("id" INTEGER PRIMARY KEY AUTOINCREMENT , "item" TEXT, "type" TEXT)"""
    _sql_push = 'INSERT INTO "justqueue" ("item", "type") VALUES (?, ?)'
    _sql_len = 'SELECT COUNT("id") FROM "justqueue"'

    def __init__(self, path, items=None):
        """
        init the queue
        :param path: the path you want to store the sqlite db file
        :param items: push some items when init the queue, iterable
        """
        self.path = os.path.abspath(path)
        self.conn = sqlite3.connect(self.path)
        with self.conn as conn:
            conn.execute(self._sql_create)
            if items:
                conn.executemany(self._sql_push, (tran_item(item) for item in items))

    def __len__(self):
        with self.conn as conn:
            size, = conn.execute(self._sql_len).fetchone()
            return size

    def close(self, remove=True):
        size = len(self)
        self.conn.close()
        if size == 0 and remove:
            os.remove(self.path)
