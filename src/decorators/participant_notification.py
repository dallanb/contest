from functools import wraps

from ..common import ParticipantStatusEnum
from ..models import Contest
from ..common import DB


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
            value = {
                'contest_uuid': str(new_instance.contest_uuid),
                'participant_uuid': str(new_instance.uuid),
                'user_uuid': str(new_instance.user_uuid),
                'owner_uuid': str(new_instance.contest.owner_uuid)
            }
            self.service.notify(topic=self.topic, value=value, key=key)

    def update(self, prev_instance, new_instance):
        if prev_instance and prev_instance['status'].name != new_instance.status.name:
            key = f'participant_{new_instance.status.name}'
            contests = DB().find(model=Contest, uuid=str(new_instance.contest_uuid))
            owner_uuid = contests.items[0].owner_uuid if contests.total else None
            value = {
                'contest_uuid': str(new_instance.contest_uuid),
                'participant_uuid': str(new_instance.uuid),
                'user_uuid': str(new_instance.user_uuid),
                'owner_uuid': str(owner_uuid)
            }
            self.service.notify(topic=self.topic, value=value, key=key)
