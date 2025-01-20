import redis.asyncio
import ring

from ring.func.asyncio import Aioredis2Storage
from pyTON.core.settings import RedisCacheSettings


class TonlibResultRedisStorage(Aioredis2Storage):
    async def set(self, key, value, expire=...):
        if value.get('@type', 'error') == 'error':
            return None
        return await super().set(key, value, expire)


class CacheManager:
    def cached(self, expire=0, check_error=True):
        pass


class DisabledCacheManager:
    def cached(self, expire=0, check_error=True):
        def g(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return g


class RedisCacheManager:
    def __init__(self, cache_settings: RedisCacheSettings):
        self.cache_settings = cache_settings
        redis_url = f"redis://{cache_settings.redis.endpoint}:{cache_settings.redis.port}"
        # if self.cache_settings.redis.timeout is not None:
        #     redis_url += '?timeout={self.cache_settings.redis.timeout}'
        self.cache_redis = redis.asyncio.from_url(redis_url)

    def cached(self, expire=0, check_error=True):
        storage_class = TonlibResultRedisStorage if check_error else Aioredis2Storage
        def g(func):
            return ring.aioredis(self.cache_redis, coder='pickle', expire=expire, storage_class=storage_class)(func)
        return g
