# -*- coding:utf-8 -*-
#
# author: yangmqglobe
# file: testfifoqueue.py
# time: 2017/6/24
from justqueue import FIFOQueue
from justqueue import exceptions
from justqueue.utils import RetryItem
import unittest
import os


class TestFIFOQueue(unittest.TestCase):
    def setUp(self):
        # remove the queue db file before test
        if os.path.exists('test'):
            os.remove('test')

    def tearDown(self):
        # try close the queue after test
        try:
            self.queue.close()
        except exceptions.QueueClosedError:
            pass

    def test_init(self):
        # make sure the queue db file can be create
        self.queue = FIFOQueue('test')
        self.assertTrue(os.path.exists('test'))

    def test_len(self):
        # make sure we can get the correct length of the queue
        self.queue = FIFOQueue('test', range(100))
        self.assertEqual(len(self.queue), 100)

    def test_auto_remove(self):
        # would not remove the queue db file since there still some items
        self.queue = FIFOQueue('test', range(100))
        self.queue.close()
        self.assertTrue(os.path.exists('test'))
        # remove the queue db file when the queue is empty
        self.queue = FIFOQueue('test', overwrite=True)
        self.queue.close()
        self.assertFalse(os.path.exists('test'))

    def test_peek(self):
        # make sure peek the correct item from the queue
        self.queue = FIFOQueue('test', range(100))
        item = self.queue.peek()
        self.assertEqual(len(self.queue), 100)
        self.assertEqual(item, 0)
        # make sure peek the correct items from the queue
        items = self.queue.peeks(10)
        self.assertEqual(len(self.queue), 100)
        for test, item in zip(range(10), items):
            self.assertEqual(test, item)

    def test_pop(self):
        # make sure pop the correct item from the queue
        self.queue = FIFOQueue('test', range(100))
        item = self.queue.pop()
        self.assertEqual(len(self.queue), 99)
        self.assertEqual(item, 0)
        # make sure pop the correct items from the queue
        items = self.queue.pops(10)
        self.assertEqual(len(self.queue), 89)
        for test, item in zip(range(1, 11), items):
            self.assertEqual(test, item)

    def test_push(self):
        # make sure item can be push into the queue
        self.queue = FIFOQueue('test')
        self.queue.push(1)
        self.assertEqual(len(self.queue), 1)
        self.assertEqual(self.queue.pop(), 1)
        # make sure items can be push into the queue
        self.queue.pushes(range(100))
        self.assertEqual(len(self.queue), 100)
        for test, item in zip(range(100), range(100)):
            self.assertEqual(test, item)

    def test_type_supported(self):
        self.queue = FIFOQueue('test')
        # make sure int is supported
        self.queue.push(1)
        self.assertEqual(self.queue.pop(), 1)
        # make sure float is supported
        self.queue.push(2.2)
        self.assertEqual(self.queue.pop(), 2.2)
        # make sure str is supported
        self.queue.push('3')
        self.assertEqual(self.queue.pop(), '3')
        # make sure list is supported
        self.queue.push([1, 2.2, '3', {'4': 4}])
        self.assertEqual(self.queue.pop(), [1, 2.2, '3', {'4': 4}])
        # make dict int is supported
        self.queue.push({'a': 1, 'b': 2.2, 'c': '3.3', 'd': [4], 'e': {'f': 'f'}})
        self.assertEqual(self.queue.pop(), {'a': 1, 'b': 2.2, 'c': '3.3', 'd': [4], 'e': {'f': 'f'}})

    def test_iter(self):
        self.queue = FIFOQueue('test', range(100))
        for test, item in zip(range(100), self.queue):
            self.assertEqual(test, item)

    def test_retry_item(self):
        self.queue = FIFOQueue('test')
        # make sure int is supported
        self.queue.push(RetryItem(1, 1))
        self.assertEqual(self.queue.pop(), 1)
        # make sure float is supported
        self.queue.push(RetryItem(2.2, 2))
        self.assertEqual(self.queue.pop(), 2.2)
        # make sure str is supported
        self.queue.push(RetryItem('3', 3))
        self.assertEqual(self.queue.pop(), '3')
        # make sure list is supported
        self.queue.push(RetryItem([1, 2.2, '3', {'4': 4}], 4))
        self.assertEqual(self.queue.pop(), [1, 2.2, '3', {'4': 4}])
        # make dict int is supported
        self.queue.push(RetryItem({'a': 1, 'b': 2.2, 'c': '3.3', 'd': [4], 'e': {'f': 'f'}}, 5))
        self.assertEqual(self.queue.pop(), {'a': 1, 'b': 2.2, 'c': '3.3', 'd': [4], 'e': {'f': 'f'}})

if __name__ == '__main__':
    unittest.main()
