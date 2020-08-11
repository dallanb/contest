from marshmallow import validate, Schema, post_dump
from webargs import fields
from marshmallow_enum import EnumField
from ....common import ContestStatusEnum


class CreateContestSchema(Schema):
    owner_uuid = fields.UUID()
    sport_uuid = fields.UUID()


class DumpContestSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    owner_uuid = fields.UUID()
    status = EnumField(ContestStatusEnum)
    participants = fields.List(fields.Nested('DumpParticipantSchema'))

    def get_attribute(self, obj, attr, default):
        if attr == 'participants':
            return getattr(obj, attr, default) if any(
                attr in include for include in self.context.get('include', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('participants', False) is None:
            del data['participants']
        return data


class FetchAllContestSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    owner_uuid = fields.UUID(required=False)


create_schema = CreateContestSchema()
dump_schema = DumpContestSchema()
dump_many_schema = DumpContestSchema(many=True)
fetch_all_schema = FetchAllContestSchema()
