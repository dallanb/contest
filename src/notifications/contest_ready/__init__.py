from .schema import ContestReadySchema
from ..base import Base


class contest_ready(Base):
    key = 'contest_ready'
    schema = ContestReadySchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, contest):
        data = cls.schema.dump({'contest': contest})
        return contest_ready(data=data)
