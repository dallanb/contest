from marshmallow import Schema, pre_dump
from webargs import fields


class ContestInactiveSchema(Schema):
    uuid = fields.UUID(attribute='contest.uuid')
    league_uuid = fields.UUID(attribute='contest.league_uuid', missing=None)
    owner_uuid = fields.UUID(attribute='contest.owner_uuid')
    message = fields.String()

    @pre_dump
    def prepare(self, data, **kwargs):
        contest = data['contest']
        data['message'] = f"{contest.name} is inactive"
        return data
