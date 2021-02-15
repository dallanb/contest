from .schema import ParticipantCompletedSchema
from ..base import Base


class participant_completed(Base):
    key = 'participant_completed'
    schema = ParticipantCompletedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, participant):
        data = cls.schema.dump({'participant': participant})
        return participant_completed(data=data)
