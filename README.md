# justqueue
## Why justqueue

Sometimes, I have to do something with an persistence queue which can make sure the whole task is finish, but most of the persistence queue is depending on Redis. What? I am just writing a simple spider! So, justqueue is light enough for some situation like that and I decide to develop it depend on built-in packege sqlite3.

## How to use it

Now, justqueue is not stable yet, so just some example here.

Create a queue

```python
from justqueue import FIFOQueue
queue = FIFOQueue('my-queue')
```

just give the path to store the queue, if the file is exist, it will load it or it will create a new queue,  sometime, you need to push some items into the queue or clear it when you create it, just use the key params

```python
queue = FIFOQueue('my-queue', items=(1, 2.2, '3', {'4': 4}), overwrite=True)
```

just make sure that the "items" is iterable and you don't need the old queue. By the way, justqueue now only support int, float, str and dict(use json),  all of this item will transform to str and store in the sqlite file, when you pop the item, justqueue will reduce it back to the type they belong to.

Get the length of the queue

```python
len(queue)
```

Push items into the queue

```python
queue.push(5)
# or push lots of items quickly
queue.pushes(range(100))
```

Peek the queue

```python
item = queue.peek()
# or peek some items
items = queue.peeks(3)
```

Pop item

```python
item = queue.pop()
# or pop some items
items = queue,pop(3)
```

when you use peeks or pops, if the queue is empty, you will get an empty generater, but when you use the peek/pop on an empty queue, will raise `EmptyQueueError`

You can iter the queue by

```python
for item in queue:
    do_something(item)
```

but make sure the task will be done safely, cos' the item is iter by pop, not peek, or you can

```python
for item in queue:
    try:
        do_something(item)
    except:
        queue.push(item)
```

Finally, do not forget to close the queue

```python
queue.close()
```

if the queue is empty, the file will be delete, if you want to keep the file, just

```python
queue.close(remove=False)
```

by the way, you can use the `with` block to make sure the queue will be closed automatic

```python
with FIFOQueue('my-queue') as queue:
    do_something(queue)
```

Get some exceptions?

All of the Exception raise by justqueue is extend from `exceptions.JustQueueError`. The `UnsupportedTypeError` would be raise when you try to push some item that is not supported, `EmptyQueueError` would be raise when you try to peek/pop from an empty queue, `QueueClosedError` would be raise when you try to operate a closed queue. 