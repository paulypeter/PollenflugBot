"""create Redis DB"""

import redis

r = redis.StrictRedis(decode_responses=True)
