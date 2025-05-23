from hashlib import sha256
import numpy as np
from settings import REDIS_CLIENT
from settings import EMBEDDER
from utils.text_normalizer import normalize_text


def embedding_to_key(embedding: np.ndarray, precision=4) -> str:
    # Round the embedding to reduce small differences
    rounded = np.round(embedding, decimals=precision)
    # Convert to bytes and hash
    return sha256(rounded.tobytes()).hexdigest()


def get_cache_key(question: str) -> str:
    """
    Instead directly caching the question raw string,
    we should cache the embedding of it as the cache key.
    """
    question = normalize_text(question)
    embedding = EMBEDDER.embed_query(question)
    return embedding_to_key(embedding)


def get_cached_answer(question: str):
    key = get_cache_key(question)
    return REDIS_CLIENT.get(key)


def cache_answer(question: str, answer: str, ttl_seconds: int = 60 * 10):
    key = get_cache_key(question)
    REDIS_CLIENT.setex(key, ttl_seconds, answer)
