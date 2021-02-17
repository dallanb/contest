from .schema import ContestInactiveSchema
from ..base import Base


class contest_inactive(Base):
    key = 'contest_inactive'
    schema = ContestInactiveSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, contest):
        data = cls.schema.dump({'contest': contest})
        return contest_inactive(data=data)
