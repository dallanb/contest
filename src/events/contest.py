import logging

from ..common import ParticipantStatusEnum
from ..services import ContestService, ContestMaterializedService, ParticipantService


class Contest:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.contest_service = ContestService()
        self.contest_materialized_service = ContestMaterializedService()
        self.participant_service = ParticipantService()

    def handle_event(self, key, data):
        if key == 'contest_created':
            self.logger.info('contest created')
            contests = self.contest_service.find(uuid=data['uuid'], include=['participants'])
            if contests.total:
                contest = contests.items[0]
                location = self.contest_service.fetch_location(uuid=str(contest['location_uuid']))
                owner = self.participant_service.fetch_member_user(user_uuid=str(contest.owner_uuid),
                                                                   league_uuid=str(
                                                                       data['league_uuid']) if data[
                                                                       'league_uuid'] else None)
                self.contest_materialized_service.create(
                    uuid=contest.uuid,
                    name=contest.name,
                    status=contest.status.name,
                    start_time=contest.start_time,
                    owner=contest.owner_uuid,
                    location=location.get('name', ''),
                    league=contest.league_uuid,
                    participants={
                        str(owner.get('uuid', '')): {
                            'member_uuid': str(owner.get('uuid', '')),
                            'display_name': owner.get('display_name', ''),
                            'status': ParticipantStatusEnum['active'].name,
                            'score': None,
                            'strokes': None,
                        }
                    }
                )
        elif key == 'contest_ready' or key == 'contest_active' or key == 'contest_inactive' or key == 'contest_completed':
            self.logger.info('contest updated')
            contests = self.contest_service.find(uuid=data['uuid'])
            if contests.total:
                contest = contests.items[0]
                self.contest_materialized_service.update(
                    uuid=contest.uuid,
                    status=contest.status.name
                )
        elif key == 'name_updated':  # TODO: look into making this a direct find and apply towards the materialized service
            contests = self.contest_service.find(uuid=data['uuid'])
            if contests.total:
                contest = contests.items[0]
                self.contest_materialized_service.update(
                    uuid=contest.uuid,
                    name=data['name']
                )
        elif key == 'start_time_updated':
            contests = self.contest_service.find(uuid=data['uuid'])
            if contests.total:
                contest = contests.items[0]
                self.contest_materialized_service.update(
                    uuid=contest.uuid,
                    start_time=data['start_time']
                )
        elif key == 'participant_active':
            participants = self.participant_service.find(uuid=data['participant_uuid'])
            if participants.total:
                participant = participants.items[0]
                contests = self.contest_materialized_service.find(uuid=data['contest_uuid'])
                if contests.total:
                    contest = contests.items[0]
                    member = self.participant_service.fetch_member(uuid=str(participant.member_uuid))
                    contest.participants[data['member_uuid']] = {
                        'member_uuid': data['member_uuid'],
                        'display_name': member.get('display_name', ''),
                        'status': ParticipantStatusEnum['active'].name,
                        'score': None,
                        'strokes': None
                    }  # maybe fix this to conform to the rest of the code
                    self.contest_materialized_service.save(instance=contest)
            self.contest_service.check_contest_status(uuid=data['contest_uuid'])
        elif key == 'participant_inactive':
            self.contest_service.check_contest_status(uuid=data['contest_uuid'])
        elif key == 'participant_completed':
            participants = self.participant_service.find(uuid=data['participant_uuid'])
            if participants.total:
                contests = self.contest_materialized_service.find(uuid=data['contest_uuid'])
                if contests.total:
                    contest = contests.items[0]
                    contest.participants[data['member_uuid']]['status'] = ParticipantStatusEnum['completed'].name
                    self.contest_materialized_service.save(instance=contest)
            self.contest_service.check_contest_status(uuid=data['contest_uuid'])
        elif key == 'avatar_created':
            contests = self.contest_service.find(uuid=data['contest_uuid'])
            if contests.total:
                contest = contests.items[0]
                self.contest_materialized_service.update(
                    uuid=contest.uuid,
                    avatar=data['s3_filename']
                )
