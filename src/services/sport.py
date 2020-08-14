import logging
from .base import Base


class Sport(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)

    @classmethod
    def handle_event(cls, key, data):
        return
