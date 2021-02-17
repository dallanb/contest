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
        data = self.clean(schema=create_schema, instance=request.form)

        contests = self.contest.find(uuid=uuid, include=['avatar'])
        if not contests.total:
            self.throw_error(http_code=self.code.NOT_FOUND)

        avatar = contests.items[0].avatar
        s3_filename = self.avatar.generate_s3_filename(contest_uuid=str(uuid))
        _ = self.avatar.upload_fileobj(file=data['avatar'], filename=s3_filename)
        if not avatar:
            avatar = self.avatar.create(s3_filename=s3_filename)
            self.contest.apply(instance=contests.items[0], avatar=avatar)
        return DataResponse(
            data={
                'avatars': self.dump(
                    schema=dump_schema,
                    instance=avatar
                )
            }
        )
