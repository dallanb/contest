from marshmallow import Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields
from ....common import ParticipantStatusEnum


class CreateParticipantSchema(Schema):
    user_uuid = fields.UUID(required=True)


class DumpParticipantSchema(Schema):
    status = EnumField(ParticipantStatusEnum)
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    user_uuid = fields.UUID()
    contest = fields.Nested('DumpContestSchema',
                            include=('uuid', 'ctime', 'mtime', 'name'))

    def get_attribute(self, obj, attr, default):
        if attr == 'contest':
            return getattr(obj, attr, default) if any(
                attr in expand for expand in self.context.get('expand', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('contest', False) is None:
            del data['contest']
        return data


class UpdateParticipantsSchema(Schema):
    status = fields.Str(required=True)


class FetchAllParticipantSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    user_uuid = fields.UUID(required=False)
    status = fields.Str(required=False)


create_schema = CreateParticipantSchema()
dump_schema = DumpParticipantSchema()
dump_many_schema = DumpParticipantSchema(many=True)
update_schema = UpdateParticipantsSchema()
fetch_all_schema = FetchAllParticipantSchema()
