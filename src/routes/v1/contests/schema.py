from marshmallow import Schema, post_dump
from marshmallow.validate import Range, Length
from marshmallow_enum import EnumField
from webargs import fields

from ..avatars.schema import DumpAvatarSchema
from ..sports.schema import DumpSportsSchema
from ....common import ContestStatusEnum, time_now


class CreateContestSchema(Schema):
    sport_uuid = fields.UUID()
    location_uuid = fields.UUID()
    league_uuid = fields.UUID(allow_none=True)
    name = fields.String()
    start_time = fields.Integer(validate=Range(min=time_now()))
    participants = fields.List(fields.UUID(), validate=Length(min=2))
    buy_in = fields.Float(validate=Range(min=0))
    payout = fields.List(fields.Float())


class DumpContestSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    owner_uuid = fields.UUID()
    name = fields.String()
    start_time = fields.Integer()
    status = EnumField(ContestStatusEnum)
    league_uuid = fields.UUID(allow_none=True)
    location_uuid = fields.UUID()
    participants = fields.List(fields.Nested('DumpParticipantSchema'))
    avatar = fields.Nested(DumpAvatarSchema)
    sport = fields.Nested(DumpSportsSchema, exclude=('contest',))

    def get_attribute(self, obj, attr, default):
        if attr == 'participants':
            return getattr(obj, attr, default) if any(
                attr in include for include in self.context.get('include', [])) else None
        if attr == 'avatar':
            return getattr(obj, attr, default) or {} if any(
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
        if data.get('avatar', False) is None:
            del data['avatar']
        if data.get('sport', False) is None:
            del data['sport']
        return data


class DumpContestMaterializedSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    name = fields.String()
    status = fields.String()
    avatar = fields.String()
    league = fields.UUID(allow_none=True)
    location = fields.String()
    owner = fields.UUID()
    participants = fields.Dict()
    start_time = fields.Integer()


class UpdateContestSchema(Schema):
    name = fields.Str(required=False)
    start_time = fields.Integer(required=False)


class FetchContestSchema(Schema):
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class FetchAllContestSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])
    league_uuid = fields.UUID(required=False)


class FetchAllContestCalendarSchema(Schema):
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])
    league_uuid = fields.UUID(required=False)
    month = fields.Int(required=True)
    year = fields.Int(required=True)


class _FetchAllContestMaterializedHasKeySchema(Schema):
    participant = fields.UUID(required=False)


class FetchAllContestMaterializedSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    search = fields.String(required=False)
    sort_by = fields.String(required=False)
    participants = fields.String(required=False, attribute="has_key.participants", data_key='participants')
    league = fields.UUID(required=False, data_key="league_uuid")


create_schema = CreateContestSchema()
dump_schema = DumpContestSchema()
dump_many_schema = DumpContestSchema(many=True)
dump_materialized_schema = DumpContestMaterializedSchema()
dump_many_materialized_schema = DumpContestMaterializedSchema(many=True)
update_schema = UpdateContestSchema()
fetch_schema = FetchContestSchema()
fetch_all_schema = FetchAllContestSchema()
fetch_all_calendar_schema = FetchAllContestCalendarSchema()
fetch_all_materialized_schema = FetchAllContestMaterializedSchema()
