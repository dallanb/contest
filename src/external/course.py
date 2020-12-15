from .base import Base
from .. import app


class Course(Base):
    def __init__(self):
        Base.__init__(self)
        self.base_url = app.config['COURSE_URL']

    def fetch_course(self, uuid):
        url = f'{self.base_url}/courses/{uuid}'
        res = self.get(url=url)
        return res.json()
