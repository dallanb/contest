from functools import wraps

from ..notifications import owner_active, participant_active, participant_completed, participant_inactive, \
    participant_invited


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
            elif self.operation == 'create_owner':
                buy_in = kwargs.pop('buy_in', None)
                payout = kwargs.pop('payout', None)
                self.create_owner(new_instance=new_instance, buy_in=buy_in, payout=payout)
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
        topic = participant_invited.topic
        key = participant_invited.key
        value = participant_invited.schema.dump({'participant': new_instance})
        self.service.notify(topic=topic, value=value, key=key)

    def create_owner(self, new_instance, buy_in, payout):
        topic = owner_active.topic
        key = owner_active.key
        value = owner_active.schema.dump({'participant': new_instance, 'buy_in': buy_in, "payout": payout})
        self.service.notify(topic=topic, value=value, key=key)

    def update(self, prev_instance, new_instance):
        if prev_instance and prev_instance['status'].name != new_instance.status.name:
            if new_instance.status.name == 'active':
                topic = participant_active.topic
                key = participant_active.key
                value = participant_active.schema.dump({'participant'})
                self.service.notify(topic=topic, value=value, key=key)
            elif new_instance.status.name == 'inactive':
                topic = participant_inactive.topic
                key = participant_inactive.key
                value = participant_inactive.schema.dump({'participant'})
                self.service.notify(topic=topic, value=value, key=key)
            elif new_instance.status.name == 'completed':
                topic = participant_completed.topic
                key = participant_completed.key
                value = participant_completed.schema.dump({'participant'})
                self.service.notify(topic=topic, value=value, key=key)
