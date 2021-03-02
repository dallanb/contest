import uuid

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

        # ensure passed in parameters are correct by requesting external api's
        location = self.contest.fetch_location(uuid=str(data['location_uuid']))
        if location is None:
            self.throw_error(http_code=self.code.BAD_REQUEST, msg='Location does not exist')

        owner = self.participant.fetch_member_user(user_uuid=str(g.user),
                                                   league_uuid=str(
                                                       data['league_uuid']) if data['league_uuid'] else None)
        if owner is None:
            self.throw_error(http_code=self.code.BAD_REQUEST, msg='User not found')
        # confirm that the owner is in the passed in participants list
        if uuid.UUID(owner['uuid']) not in data['participants']:
            self.throw_error(http_code=self.code.BAD_REQUEST, msg='Owner should be included in the participants')

        # create contest
        contest = self.contest.create(status='pending', owner_uuid=owner['user_uuid'], name=data['name'],
                                      start_time=data['start_time'], location_uuid=data['location_uuid'],
                                      league_uuid=data['league_uuid'])
        # create sport
        _ = self.sport.create(sport_uuid=data['sport_uuid'], contest=contest)

        # create owner
        # remove the owner from the participants
        data['participants'].remove(uuid.UUID(owner['uuid']))
        _ = self.participant.create_owner(member_uuid=owner['uuid'], contest=contest, buy_in=data['buy_in'],
                                          payout=data['payout'])

        # create other participants in a separate thread cause it is not critical if they are created right away
        self.participant.create_batch_threaded(uuids=data['participants'], contest=contest)
        return DataResponse(
            data={
                'contests': self.dump(
                    schema=dump_schema,
                    instance=contest
                )
            }
        )


class ContestsListCalendarAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.contest = ContestService()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_calendar_schema, instance=request.args)
        contests = self.contest.find_by_start_time_range(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=contests.total,
                ),
                'contests': self.dump(
                    schema=dump_many_schema,
                    instance=contests.items,
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
