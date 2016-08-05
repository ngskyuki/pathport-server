# -*- coding: utf-8 -*-

import os

# packages for redis
import redis
from rq import Worker, Queue, Connection

# configuration for Redis
listen = ['default']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
print(redis_url)
conn = redis.from_url(redis_url)

if __name__ == '__main__':
  with Connection(conn):
    worker = Worker(list(map(Queue, listen)))
    worker.work()

