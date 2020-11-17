import logging
from .base import Base
from ..models import Location as LocationModel


class Location(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.location_model = LocationModel

    def find(self, **kwargs):
        return Base.find(self, model=self.location_model, **kwargs)

    def create(self, **kwargs):
        location = self.init(model=self.location_model, **kwargs)
        return self.save(instance=location)
