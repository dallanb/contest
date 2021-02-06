from .base import Base
from .. import app


class Wager(Base):
    def __init__(self):
        Base.__init__(self)
        self.base_url = app.config['WAGER_URL']

    def get_contest(self, uuid):
        url = f'{self.base_url}/contests/{uuid}/complete'
        res = self.get(url=url)
        return res.json()
