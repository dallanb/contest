from marshmallow import Schema, pre_dump
from webargs import fields


class ContestReadySchema(Schema):
    uuid = fields.UUID()
    league_uuid = fields.UUID(missing=None)
    owner_uuid = fields.UUID()
    message = fields.String()

    @pre_dump
    def generate_message(self, data, **kwargs):
        name = data.get('name', '')
        setattr(data, 'message', f"{name} is ready")
        return
