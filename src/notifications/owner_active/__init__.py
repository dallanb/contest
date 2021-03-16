from .schema import OwnerActiveSchema
from ..base import Base


class owner_active(Base):
    key = 'owner_active'
    schema = OwnerActiveSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, participant, buy_in, payout):
        data = cls.schema.dump({'participant': participant, 'buy_in': buy_in, 'payout': payout})
        return owner_active(data=data)
