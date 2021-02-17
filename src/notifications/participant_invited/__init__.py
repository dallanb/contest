from .schema import ParticipantInvitedSchema
from ..base import Base


class participant_invited(Base):
    key = 'participant_invited'
    schema = ParticipantInvitedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, participant):
        data = cls.schema.dump({'participant': participant})
        return participant_invited(data=data)
