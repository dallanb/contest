from marshmallow import Schema, pre_dump
from webargs import fields

from src import services, Contest
from src.common import DB, ManualException


class ParticipantCompletedSchema(Schema):
    contest_uuid = fields.UUID(attribute='participant.contest_uuid')
    participant_uuid = fields.UUID(attribute='participant.uuid')
    member_uuid = fields.UUID(attribute='participant.member_uuid')
    user_uuid = fields.UUID(attribute='member.user_uuid')
    owner_uuid = fields.UUID(attribute='contest.owner_uuid')
    league_uuid = fields.UUID(attribute='contest.league_uuid', missing=None)
    message = fields.String()

    @pre_dump
    def prepare(self, data, **kwargs):
        contests = DB().find(model=Contest, uuid=str(data['participant'].contest_uuid))
        contest = contests.items[0]
        member = services.ParticipantService().fetch_member(uuid=str(data['participant'].member_uuid))
        if member is None:
            raise ManualException(err=f'member with uuid: {str(data["participant"].member_uuid)} not found')

        data['contest'] = contest
        data['member'] = member
        data['message'] = f"{member['display_name']} completed {contest.name}"
        return data
