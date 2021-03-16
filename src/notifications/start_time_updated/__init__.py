from .schema import StartTimeUpdatedSchema
from ..base import Base


class start_time_updated(Base):
    key = 'start_time_updated'
    schema = StartTimeUpdatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, contest):
        data = cls.schema.dump({'contest': contest})
        return start_time_updated(data=data)
