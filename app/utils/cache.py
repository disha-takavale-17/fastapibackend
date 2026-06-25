import redis, json

# connects to local redis server
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# fetches value from db using key
def get_cache(key: str):
    cached = redis_client.get(key)
    # deserializes json back into python dic
    return json.loads(cached) if cached else None

# stores specific book in redis with ttl
def set_cache(key: str, value: dict, ttl: int = 600):
    redis_client.setex(key, ttl, json.dumps(value))

def delete_cache(key: str):
    redis_client.delete(key)

def increment_popularity(title: str):
    # Track how many times a book is requested
    redis_client.zincrby("popular_books", 1, title.lower())

# we cna use it later to display popular books
def get_top_books(n: int = 10):
    # Return top N most requested titles
    return redis_client.zrevrange("popular_books", 0, n-1)
