from flask import request, g
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.auth import check_user
from ....common.response import DataResponse
from ....services import Contest, Sport, Participant


class ContestsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.contest = Contest()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        data = self.clean(schema=fetch_schema, instance=request.args)
        contests = self.contest.find(uuid=uuid, **data)
        if not contests.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'contests': self.dump(
                    schema=dump_schema,
                    instance=contests.items[0],
                    params={
                        'include': data['include'],
                        'expand': data['expand']
                    }
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    def put(self, uuid):
        data = self.clean(schema=update_schema, instance=request.get_json())
        contest = self.contest.update(uuid=uuid, **data)
        return DataResponse(
            data={
                'contests': self.dump(
                    schema=dump_schema,
                    instance=contest
                )
            }
        )


class ContestsListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.contest = Contest()
        self.sport = Sport()
        self.participant = Participant()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        contests = self.contest.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=contests.total,
                    page_count=len(contests.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'contests': self.dump(
                    schema=dump_many_schema,
                    instance=contests.items,
                    params={
                        'include': data['include'],
                        'expand': data['expand']
                    }
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self):
        data = self.clean(schema=create_schema, instance=request.get_json())
        contest = self.contest.create(status='pending', owner_uuid=data['owner_uuid'], name=data['name'],
                                      start_time=data['start_time'])
        _ = self.sport.create(sport_uuid=data['sport_uuid'], contest=contest)

        participants = data.pop('participants')
        if participants:
            for user_uuid in participants:
                status = 'active' if g.user == user_uuid else 'pending'
                self.participant.create(user_uuid=user_uuid, status=status, contest=contest)
        return DataResponse(
            data={
                'contests': self.dump(
                    schema=dump_schema,
                    instance=contest
                )
            }
        )
