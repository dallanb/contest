import logging
from ..services import ContestService, ContestMaterializedService, ParticipantService


class Score:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.contest_service = ContestService()
        self.contest_materialized_service = ContestMaterializedService()
        self.participant_service = ParticipantService()

    def handle_event(self, key, data):
        if key == 'stroke_update':
            contests = self.contest_materialized_service.find(uuid=data['contest_uuid'])
            if contests.total:
                contest = contests.items[0]
                contest.participants[data['participant_uuid']]['score'] = data['strokes']
                self.contest_materialized_service.save(instance=contest)
