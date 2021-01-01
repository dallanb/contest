from flask import request, g
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.auth import check_user
from ....common.response import DataResponse
from ....services import ContestService, SportService, ParticipantService, ContestMaterializedService


class ContestsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.contest = ContestService()

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
        self.contest = ContestService()
        self.contest_materialized = ContestMaterializedService()
        self.sport = SportService()
        self.participant = ParticipantService()

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
        contest = self.contest.create(status='pending', owner_uuid=g.user, name=data['name'],
                                      start_time=data['start_time'], location_uuid=data['location_uuid'],
                                      league_uuid=data['league_uuid'])
        _ = self.sport.create(sport_uuid=data['sport_uuid'], contest=contest)
        owner = self.participant.fetch_owner(user_uuid=str(g.user), league_uuid=)

        participants = data.pop('participants')
        if participants:
            str_participants = [str(participant) for participant in participants]
            self.participant.fetch_members(uuids=str_participants)
            for member_uuid in participants:
                status = 'active' if g.user == user_uuid else 'pending'
                self.participant.create(user_uuid=user_uuid, status=status, contest=contest)

        location = self.contest.fetch_location(uuid=str(contest.location_uuid))
        # instead of creating materialized contest asynchronously we will create it when the contest is created
        self.contest_materialized.create(
            uuid=contest.uuid, name=contest.name, status=contest.status.name, start_time=contest.start_time,
            owner=contest.owner_uuid, location=location.get('name', ''), participants={str(contest.owner_uuid): {
                'uuid': str(contest.owner_uuid),
                'display_name': account.get('display_name', ''),
                'score': None,
                'strokes': None,
            }}
        )
        return DataResponse(
            data={
                'contests': self.dump(
                    schema=dump_schema,
                    instance=contest
                )
            }
        )


class ContestsMaterializedAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.contest_materialized = ContestMaterializedService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        contests = self.contest_materialized.find(uuid=uuid)
        if not contests.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'contests': self.dump(
                    schema=dump_materialized_schema,
                    instance=contests.items[0],
                )
            }
        )


class ContestsMaterializedListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.contest_materialized = ContestMaterializedService()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_materialized_schema, instance=request.args)
        contests = self.contest_materialized.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=contests.total,
                    page_count=len(contests.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'contests': self.dump(
                    schema=dump_many_materialized_schema,
                    instance=contests.items,
                )
            }
        )
