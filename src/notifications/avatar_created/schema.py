from marshmallow import Schema
from webargs import fields


class AvatarCreatedSchema(Schema):
    league_uuid = fields.UUID(missing=None, attribute='contest.league_uuid')
    owner_uuid = fields.UUID(attribute='contest.owner_uuid')
    contest_uuid = fields.UUID(attribute='contest.uuid')
    uuid = fields.UUID(attribute='avatar.uuid')
    s3_filename = fields.Str(attribute='avatar.s3_filename')
