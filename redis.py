import redis
from fastapi import Depends


redis_client = redis.Redis(host="redis", port=6379, db=0)


def store_token(user_id: str, token: str):
    redis_client.set(user_id, token, ex=3600)


def get_token(user_id: str):
    return redis_client.get(user_id)