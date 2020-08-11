from flask import request, g
from flask_restful import marshal_with
from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from ....models import Contest, Sport


class ContestsAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        contests = self.find(model=Contest, uuid=uuid, not_found=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'contests': self.dump(
                    schema=dump_schema,
                    instance=contests.items[0]
                )
            }
        )


class ContestsListAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        contests = self.find(model=Contest, **data)
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
                        'include': data['include']
                    }
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    @check_user
    def post(self):
        data = self.clean(schema=create_schema, instance=request.get_json())
        contest = self.init(model=Contest, status='pending', owner_uuid=g.user)
        sport = self.init(model=Sport, sport_uuid=data['sport_uuid'], contest=contest)
        contest = self.save(instance=contest)
        _ = self.save(instance=sport)
        return DataResponse(
            data={
                'contests': self.dump(
                    schema=dump_schema,
                    instance=contest
                )
            }
        )