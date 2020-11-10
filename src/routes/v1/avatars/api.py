from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.auth import check_user
from ....common.response import DataResponse
from ....services import AvatarService, ContestService


class AvatarsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.avatar = AvatarService()
        self.contest = ContestService()

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, uuid):
        data = self.clean(schema=create_schema, instance={**request.files.to_dict(), 'uuid': uuid})

        contests = self.contest.find(uuid=uuid, include=['avatar'])
        if not contests.total:
            self.throw_error(http_code=self.code.NOT_FOUND)

        avatar = contests.items[0].avatar
        if avatar:
            # preserve original s3_filename but replace the filename to the filename of the new file
            data['avatar'].filename = avatar.s3_filename
            _ = self.avatar.upload_fileobj(file=data['avatar'])
            avatar = self.avatar.apply(instance=avatar, filename=avatar.filename)
        else:
            _ = self.avatar.upload_fileobj(file=data['avatar'])
            avatar = self.avatar.create(filename=data['filename'], s3_filename=data['s3_filename'])
            self.contest.apply(instance=contests.items[0], avatar=avatar)
        return DataResponse(
            data={
                'avatars': self.dump(
                    schema=dump_schema,
                    instance=avatar
                )
            }
        )
