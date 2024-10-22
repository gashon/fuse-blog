import threading
import time

from api_client import BlogAPIClient


class Cache:
    def __init__(self, ttl=300):
        self.ttl = ttl  # Time-to-live for cache
        self.lock = threading.Lock()
        self.posts = {}
        self.last_updated = 0

    def get_posts(self):
        with self.lock:
            if time.time() - self.last_updated > self.ttl:
                self.update_cache()
            return self.posts

    def update_cache(self):
        client = BlogAPIClient()
        data = client.get_posts(limit=100)
        posts = data.get('data', [])
        self.posts = {
            self.format_filename(post): post
            for post in posts
            if not post.get('is_private')
        }
        self.last_updated = time.time()

    @staticmethod
    def format_filename(post):
        timestamp = time.strftime(
            '%Y-%m-%d_%H-%M-%S', time.localtime(post['created_at'] / 1000)
        )
        filename = f"{timestamp}_{post['post_id']}.txt"
        return filename

