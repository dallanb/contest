import logging

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
        elif key == 'contest_ready' or key == 'contest_active' or key == 'contest_inactive':
            self.logger.info('contest updated')
            contests = self.contest_service.find(uuid=data['uuid'])
            if contests.total:
                contest = contests.items[0]
                self.contest_materialized_service.update(
                    uuid=contest.uuid,
                    status=contest.status.name
                )
        elif key == 'name_updated':
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
                    account = self.participant_service.fetch_account(uuid=str(participant.user_uuid))
                    contest.participants[data['user_uuid']] = {
                        'first_name': account['first_name'],
                        'last_name': account['last_name'],
                        'score': None,
                        'strokes': None
                    }  # maybe fix this to conform to the rest of the code
                    self.contest_materialized_service.save(instance=contest)
            self.contest_service.check_contest_status(uuid=data['contest_uuid'])
        elif key == 'participant_inactive':
            self.contest_service.check_contest_status(uuid=data['contest_uuid'])
        elif key == 'participant_completed':
            self.contest_service.check_contest_status(uuid=data['contest_uuid'])
        elif key == 'avatar_created':
            contests = self.contest_service.find(uuid=data['contest_uuid'])
            if contests.total:
                contest = contests.items[0]
                self.contest_materialized_service.update(
                    uuid=contest.uuid,
                    avatar=data['s3_filename']
                )
