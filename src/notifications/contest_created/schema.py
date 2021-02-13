from marshmallow import Schema
from webargs import fields


class ContestCreatedSchema(Schema):
    uuid = fields.UUID()
    league_uuid = fields.UUID(missing=None)
    owner_uuid = fields.UUID()
