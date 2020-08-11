from marshmallow import fields, Schema


class DumpSportsSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    contest = fields.Nested('DumpContestSchema')
    sport_uuid = fields.UUID()


dump_schema = DumpSportsSchema()
dump_many_schema = DumpSportsSchema(many=True)
