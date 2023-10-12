import redis

from app.core.config import settings


class RedisCRUD:
    def __init__(self, host: str, port: int, password: str, db: int):
        self.redis_client = redis.StrictRedis(
            host=host, password=password, port=port, db=db
        )

    def create(self, key, value, expiration_seconds):
        self.redis_client.setex(key, expiration_seconds, value)

    def read(self, key):
        return self.redis_client.get(key)

    def exist(self, key):
        return self.redis_client.exists(key)

    def update(self, key, new_value):
        if self.redis_client.exists(key):
            self.redis_client.set(key, new_value)
        else:
            print(f"Key '{key}' does not exist in Redis.")

    def delete(self, key):
        if self.redis_client.exists(key):
            self.redis_client.delete(key)
        else:
            print(f"Key '{key}' does not exist in Redis.")


redis_conn = RedisCRUD(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    db=settings.REDIS_DB,
)
