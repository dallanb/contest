from marshmallow import Schema, pre_dump
from webargs import fields


class ContestActiveSchema(Schema):
    uuid = fields.UUID(attribute='contest.uuid')
    league_uuid = fields.UUID(attribute='contest.league_uuid', missing=None)
    owner_uuid = fields.UUID(attribute='contest.owner_uuid')
    message = fields.String()

    @pre_dump
    def prepare(self, data, **kwargs):
        name = data.get('name', '')
        data['message'] = f"{name} is active"
        return data