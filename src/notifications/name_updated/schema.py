from marshmallow import Schema
from webargs import fields


class NameUpdatedSchema(Schema):
    uuid = fields.UUID()
    league_uuid = fields.UUID(missing=None)
    name = fields.String()
