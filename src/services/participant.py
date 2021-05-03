import concurrent.futures
import logging
import threading
import time
from http import HTTPStatus

from .base import Base
from ..decorators.notifications import participant_notification
from ..external import Member as MemberExternal
from ..models import Participant as ParticipantModel
from ..services import ContestService


class Participant(Base):

    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.participant_model = ParticipantModel

    def find(self, **kwargs):
        return self._find(model=self.participant_model, **kwargs)

    def init(self, **kwargs):
        return self._init(model=self.participant_model, **kwargs)

    @participant_notification(operation='create')
    def create(self, **kwargs):
        participant = self._init(model=self.participant_model, **kwargs)
        return self._save(instance=participant)

    def update(self, uuid, **kwargs):
        participants = self.find(uuid=uuid)
        if not participants.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=participants.items[0], **kwargs)

    @participant_notification(operation='update')
    def apply(self, instance, **kwargs):
        # if contest status is being updated we will trigger a notification
        _ = self._status_machine(instance.status.name, kwargs.get('status'))
        participant = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=participant)

    @participant_notification(operation='create_owner')
    def create_owner(self, buy_in, payout, **kwargs):
        owner = self._init(model=self.participant_model, **kwargs, status='active')
        return self._save(instance=owner)

    def create_batch(self, uuids, contest):
        participants = [str(uuid) for uuid in uuids]
        member_batch = self.fetch_member_batch(uuids=participants)
        for member in member_batch:
            if member is None:
                # send a notifications here
                self.create(member_uuid=None, status='inactive', contest=contest)
            else:
                self.create(member_uuid=member['uuid'], status='pending', contest=contest)
        ContestService().check_contest_status(uuid=contest.uuid)

    def create_batch_threaded(self, uuids, contest):
        thread = threading.Thread(target=self.create_batch, args=(uuids, contest),
                                  daemon=True)
        thread.start()

    def _status_machine(self, prev_status, new_status):
        # cannot go from active to pending
        if prev_status == 'active' and new_status == 'pending':
            self.error(code=HTTPStatus.BAD_REQUEST)
        return True

    def fetch_member_user(self, user_uuid, league_uuid):
        hit = self.cache.get(f'{user_uuid}_{league_uuid}')
        if hit:
            return hit
        try:
            res = MemberExternal().fetch_member_user(uuid=user_uuid, params={'league_uuid': league_uuid})
            member = res['data']['members']
            self.cache.set(f'{user_uuid}_{league_uuid}', member, 3600)
            self.cache.set(str(member['uuid']), member, 3600)
            return member
        except TypeError:
            return None

    # possibly turn this into a decorator (the caching part)
    def fetch_member(self, uuid):
        hit = self.cache.get(uuid)
        if hit:
            return hit
        try:
            res = MemberExternal().fetch_member(uuid=uuid)
            member = res['data']['members']
            self.cache.set(f'{str(member["user_uuid"])}_{str(member["league_uuid"])}', member, 3600)
            self.cache.set(uuid, member, 3600)
            return member
        except TypeError:
            return None

    def fetch_member_batch(self, uuids):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            batch = executor.map(self.fetch_member, uuids)
        return batch
