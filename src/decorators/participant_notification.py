from functools import wraps

from ..common import DB
from ..common import ParticipantStatusEnum
from ..models import Contest


class participant_notification:
    def __init__(self, operation):
        self.operation = operation
        self.topic = 'contests'
        self._service = None

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            self.service = args[0]
            prev_instance = {**kwargs['instance'].__dict__} if kwargs.get('instance') else None
            new_instance = f(*args, **kwargs)
            if self.operation == 'create':
                self.create(new_instance=new_instance)
            elif self.operation == 'update':
                self.update(prev_instance=prev_instance, new_instance=new_instance)
            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, service):
        self._service = service

    def create(self, new_instance):
        if new_instance.status == ParticipantStatusEnum['pending']:
            key = 'participant_invited'
            contests = DB().find(model=Contest, uuid=str(new_instance.contest_uuid))
            contest = contests.items[0]
            member = self.service.fetch_member(uuid=str(new_instance.member_uuid))
            value = {
                'contest_uuid': str(new_instance.contest_uuid),
                'participant_uuid': str(new_instance.uuid),
                'member_uuid': str(new_instance.member_uuid),
                'user_uuid': str(member['user_uuid']),
                'owner_uuid': str(contest.owner_uuid),
                'message': self.generate_message(key=key, contest=contest)
            }
            self.service.notify(topic=self.topic, value=value, key=key)

    def update(self, prev_instance, new_instance):
        if prev_instance and prev_instance['status'].name != new_instance.status.name:
            key = f'participant_{new_instance.status.name}'
            contests = DB().find(model=Contest, uuid=str(new_instance.contest_uuid))
            contest = contests.items[0]
            member = self.service.fetch_member(uuid=str(new_instance.member_uuid))
            value = {
                'contest_uuid': str(new_instance.contest_uuid),
                'participant_uuid': str(new_instance.uuid),
                'member_uuid': str(new_instance.member_uuid),
                'user_uuid': str(member['user_uuid']),
                'owner_uuid': str(contest.owner_uuid),
                'message': self.generate_message(key=key, contest=contest, member=new_instance)
            }
            self.service.notify(topic=self.topic, value=value, key=key)

    def generate_message(self, key, **kwargs):
        if key == 'participant_invited':
            contest = kwargs.get('contest')
            owner = self.service.fetch_member_user(
                user_uuid=str(contest.owner_uuid),
                league_uuid=str(contest.league_uuid) if contest.league_uuid else None
            )
            return f"{owner['display_name']} invited you to {contest.name}"
        elif key == 'participant_active':
            contest = kwargs.get('contest')
            member = kwargs.get('member')
            return f"{member['display_name']} accepted invite to {contest.name}"
        elif key == 'participant_inactive':
            contest = kwargs.get('contest')
            member = kwargs.get('member')
            return f"{member['display_name']} declined invite to {contest.name}"
        else:
            return ''
