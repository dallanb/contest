from marshmallow import Schema
from webargs import fields


class StartTimeUpdatedSchema(Schema):
    uuid = fields.UUID()
    league_uuid = fields.UUID(missing=None)
    start_time = fields.Int()
