import logging
from functools import wraps

from ..notifications import owner_active, participant_active, participant_completed, participant_inactive, \
    participant_invited


class participant_notification:
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
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

    @staticmethod
    def create(new_instance):
        participant_invited.from_data(participant=new_instance).notify()

    @staticmethod
    def create_owner(new_instance, buy_in, payout):
        owner_active.from_data(participant=new_instance, buy_in=buy_in, payout=payout).notify()

    @staticmethod
    def update(prev_instance, new_instance):
        if prev_instance and prev_instance['status'].name != new_instance.status.name:
            if new_instance.status.name == 'active':
                participant_active.from_data(participant=new_instance).notify()
            elif new_instance.status.name == 'inactive':
                participant_inactive.from_data(participant=new_instance).notify()
            elif new_instance.status.name == 'completed':
                participant_completed.from_data(participant=new_instance).notify()
