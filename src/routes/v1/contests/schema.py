from marshmallow import Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields

from ..sports.schema import DumpSportsSchema
from ....common import ContestStatusEnum


class CreateContestSchema(Schema):
    owner_uuid = fields.UUID()
    sport_uuid = fields.UUID()
    name = fields.String()
    participants = fields.List(fields.UUID(), missing=None)


class DumpContestSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    owner_uuid = fields.UUID()
    name = fields.String()
    status = EnumField(ContestStatusEnum)
    participants = fields.List(fields.Nested('DumpParticipantSchema'))
    sport = fields.Nested(DumpSportsSchema, exclude=('contest',))

    def get_attribute(self, obj, attr, default):
        if attr == 'participants':
            return getattr(obj, attr, default) if any(
                attr in include for include in self.context.get('include', [])) else None
        if attr == 'sport':
            return getattr(obj, attr, default) if any(
                attr in expand for expand in self.context.get('expand', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('participants', False) is None:
            del data['participants']
        if data.get('sport', False) is None:
            del data['sport']
        return data


class UpdateContestSchema(Schema):
    name = fields.Str(required=False)
    status = fields.Str(required=False)


class FetchContestSchema(Schema):
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class FetchAllContestSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])
    owner_uuid = fields.UUID(required=False)


create_schema = CreateContestSchema()
dump_schema = DumpContestSchema()
dump_many_schema = DumpContestSchema(many=True)
update_schema = UpdateContestSchema()
fetch_schema = FetchContestSchema()
fetch_all_schema = FetchAllContestSchema()
