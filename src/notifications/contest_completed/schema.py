from marshmallow import Schema, pre_dump
from webargs import fields


class ContestCompletedSchema(Schema):
    uuid = fields.UUID(attribute='contest.uuid')
    league_uuid = fields.UUID(attribute='contest.league_uuid', missing=None)
    owner_uuid = fields.UUID(attribute='contest.owner_uuid')
    message = fields.String()

    @pre_dump
    def prepare(self, data, **kwargs):
        contest = data['contest']
        name = contest.get('name', '')
        data['message'] = f"{name} is completed"
        return data
