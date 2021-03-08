import redis
from decouple import config
from utils.Singleton import singleton


@singleton
class Redis:
    def __init__(self):
        Redis.pool = redis.ConnectionPool(
            host=config('REDIS_HOST'),
            port=config('REDIS_PORT'),
            db=config('REDIS_DB_INDEX', 0),
            password=config('REDIS_PASSWORD'),
            decode_responses=True)
        self.db = redis.Redis(connection_pool=Redis.pool)


if __name__ == '__main__':
    redis = Redis()
    redis.db.lpush('test', 'aaa')
    print(redis.db.rpop('test'))
