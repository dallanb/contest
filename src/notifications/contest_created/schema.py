from marshmallow import Schema
from webargs import fields


class ContestCreatedSchema(Schema):
    uuid = fields.UUID(attribute='contest.uuid')
    league_uuid = fields.UUID(attribute='contest.league_uuid', missing=None)
    owner_uuid = fields.UUID(attribute='contest.owner_uuid')
