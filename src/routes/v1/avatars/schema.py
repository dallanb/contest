from flask import g
from marshmallow import validate, Schema, post_dump, pre_load
from webargs import fields
from werkzeug.utils import secure_filename
from ....common import allowed_file, file_extension


class CreateAvatarSchema(Schema):
    avatar = fields.Field()
    filename = fields.String()
    s3_filename = fields.String()

    @pre_load
    def clean_avatar(self, in_data, **kwargs):
        avatar = in_data['avatar']
        assert allowed_file(avatar.filename), "Invalid file type"
        in_data['filename'] = secure_filename(avatar.filename)
        in_data['s3_filename'] = f"{in_data['uuid']}.{file_extension(avatar.filename)}"
        in_data['avatar'].filename = in_data['s3_filename']
        # remove uuid now that it has been used
        del in_data['uuid']
        return in_data


class DumpAvatarSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    filename = fields.String()
    s3_filename = fields.String()

    def get_attribute(self, obj, attr, default):
        return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        return data


class FetchAvatarSchema(Schema):
    filename = fields.String()
    s3_filename = fields.String()


dump_schema = DumpAvatarSchema()
dump_many_schema = DumpAvatarSchema(many=True)
fetch_schema = FetchAvatarSchema()
create_schema = CreateAvatarSchema()
