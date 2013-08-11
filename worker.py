from rq import Connection, Queue, Worker

import os
import redis

listen = ['default', 'high', 'low']

redis_url = os.getenv('REDISTOGO_URL', 
  'redis://redistogo:4464813aee83f9bf7bd4a0b288191f1a@dory.redistogo.com:9458')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()