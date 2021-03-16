from .schema import ContestActiveSchema
from ..base import Base


class contest_active(Base):
    key = 'contest_active'
    schema = ContestActiveSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, contest):
        data = cls.schema.dump({'contest': contest})
        return contest_active(data=data)
