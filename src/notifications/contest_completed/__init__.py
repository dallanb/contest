from .schema import ContestCompletedSchema

from ..base import Base


class contest_completed(Base):
    key = 'contest_completed'
    schema = ContestCompletedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, contest):
        data = cls.schema.dump({'contest': contest})
        return contest_completed(data=data)
