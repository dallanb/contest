from marshmallow import Schema, pre_dump
from webargs import fields


class ContestCompletedSchema(Schema):
    uuid = fields.UUID(attribute='uuid')
    league_uuid = fields.UUID(attribute='league_uuid', missing=None)
    owner_uuid = fields.UUID(attribute='owner_uuid')
    message = fields.String()

    @pre_dump
    def prepare(self, data, **kwargs):
        name = data.get('name', '')
        data['message'] = f"{name} is completed"
        return data
