from queue import Queue
q = Queue(maxsize=2)
q.put(1)
q.put(2)
q.put(3)
print(list(q.queue))
print(q.full())  # Prints: True
