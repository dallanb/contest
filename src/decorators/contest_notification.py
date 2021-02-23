from functools import wraps

from src.notifications import contest_created, contest_ready, contest_inactive, contest_active, avatar_created, \
    name_updated, start_time_updated, contest_completed


class contest_notification:
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            prev_instance = {**kwargs.get('instance').__dict__} if kwargs.get('instance') else None
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)
            if self.operation == 'update':
                self.update(prev_instance=prev_instance, new_instance=new_instance, args=kwargs)

            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @staticmethod
    def create(new_instance):
        contest_created.from_data(contest=new_instance).notify()

    @staticmethod
    def update(prev_instance, new_instance, args):
        if prev_instance and prev_instance.get('status') and prev_instance['status'].name != new_instance.status.name:
            if new_instance.status.name == 'ready':
                contest_ready.from_data(contest=new_instance).notify()
            elif new_instance.status.name == 'active':
                contest_active.from_data(contest=new_instance).notify()
            elif new_instance.status.name == 'completed':
                contest_completed.from_data(contest=new_instance).notify()
            elif new_instance.status.name == 'inactive':
                contest_inactive.from_data(contest=new_instance).notify()
        if args.get('avatar'):
            avatar_created.from_data(contest=new_instance, avatar=args['avatar']).notify()
        if prev_instance and prev_instance.get('name') and prev_instance['name'] != new_instance.name:
            name_updated.from_data(contest=new_instance).notify()
        if prev_instance and prev_instance.get('start_time') and prev_instance['start_time'] != new_instance.start_time:
            start_time_updated.from_data(contest=new_instance).notify()
