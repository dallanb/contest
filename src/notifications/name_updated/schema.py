from marshmallow import Schema
from webargs import fields


class NameUpdatedSchema(Schema):
    uuid = fields.UUID(attribute='contest.uuid')
    league_uuid = fields.UUID(attribute='contest.league_uuid', missing=None)
    name = fields.String(attribute='contest.name')
