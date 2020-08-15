import logging
from .base import Base
from ..models import Sport as SportModel


class Sport(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.sport_model = SportModel

    def find(self, **kwargs):
        return Base.find(self, model=self.sport_model, **kwargs)

    def create(self, **kwargs):
        sport = self.init(model=self.sport_model, **kwargs)
        return self.save(instance=sport)
