import requests


class BlogAPIClient:
    def __init__(self, base_url='https://stream.ghussein.org/api'):
        self.base_url = base_url
        self.session = requests.Session()

    def get_posts(self, limit=20, cursor=None):
        params = {'limit': limit}
        if cursor:
            params['cursor'] = cursor
        response = self.session.get(f'{self.base_url}/posts', params=params)
        response.raise_for_status()
        return response.json()

