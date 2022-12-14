import redis
from settings import REDIS_HOST, REDIS_PORT

def make_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)