from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.auth import check_user
from ....common.response import DataResponse
from ....services import ParticipantService, ContestService


class ParticipantsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.participant = ParticipantService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        participants = self.participant.find(uuid=uuid)
        if not participants.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'participants': self.dump(
                    schema=dump_schema,
                    instance=participants.items[0]
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    def put(self, uuid):
        data = self.clean(schema=update_schema, instance=request.get_json())
        participant = self.participant.update(uuid=uuid, **data)
        return DataResponse(
            data={
                'participants': self.dump(
                    schema=dump_schema,
                    instance=participant
                )
            }
        )


class ParticipantsMemberAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.participant = ParticipantService()

    @marshal_with(DataResponse.marshallable())
    def get(self, contest_uuid, member_uuid):
        participants = self.participant.find(member_uuid=member_uuid, contest_uuid=contest_uuid)
        if not participants.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'participants': self.dump(
                    schema=dump_schema,
                    instance=participants.items[0]
                )
            }
        )


class ParticipantsListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.participant = ParticipantService()
        self.contest = ContestService()

    @marshal_with(DataResponse.marshallable())
    def get(self, **kwargs):
        data = self.clean(schema=fetch_all_schema, instance={**request.args, **kwargs})
        participants = self.participant.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=participants.total,
                    page_count=len(participants.items),
                    page=data['page'],
                    per_page=data['per_page']
                ),
                'participants': self.dump(
                    schema=dump_many_schema,
                    instance=participants.items,
                    params={
                        'expand': data['expand'],
                        'include': data['include']
                    }
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self, contest_uuid):
        data = self.clean(schema=create_schema, instance=request.get_json())
        contests = self.contest.find(uuid=contest_uuid)
        if not contests.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        self.participant.fetch_member(uuid=str(data['member_uuid']))
        participant = self.participant.create(member_uuid=data['member_uuid'], contest=contests.items[0],
                                              status="pending")
        return DataResponse(
            data={
                'participants': self.dump(
                    schema=dump_schema,
                    instance=participant
                )
            }
        )
