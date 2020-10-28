from .base import Base
from .. import app


class Account(Base):
    def __init__(self):
        Base.__init__(self)
        self.base_url = app.config['ACCOUNT_URL']

    def fetch_account(self, uuid):
        url = f'{self.base_url}/accounts/{uuid}'
        res = self.get(url=url)
        return res.json()
