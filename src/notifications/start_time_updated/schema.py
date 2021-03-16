from marshmallow import Schema
from webargs import fields


class StartTimeUpdatedSchema(Schema):
    uuid = fields.UUID(attribute='contest.uuid')
    league_uuid = fields.UUID(attribute='contest.league_uuid', missing=None)
    start_time = fields.Int(attribute='contest.start_time')
