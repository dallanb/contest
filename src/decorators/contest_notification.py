from functools import wraps

from src.notifications import contest_created, contest_ready, contest_inactive, contest_active, avatar_created, \
    name_updated, start_time_updated, contest_completed


class contest_notification:
    def __init__(self, operation):
        self.topic = 'contests'
        self.operation = operation
        self._service = None

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            self.service = args[0]
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

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, service):
        self._service = service

    def create(self, new_instance):
        topic = contest_created.topic
        key = contest_created.key
        value = contest_created.schema.dump({'contest': new_instance})
        self.service.notify(topic=topic, value=value, key=key, )

    def update(self, prev_instance, new_instance, args):
        if prev_instance and prev_instance.get('status') and prev_instance['status'].name != new_instance.status.name:
            if new_instance.status.name == 'ready':
                topic = contest_ready.topic
                key = contest_ready.key
                value = contest_ready.schema.dump({'contest': new_instance})
                self.service.notify(topic=topic, value=value, key=key)
            elif new_instance.status.name == 'active':
                topic = contest_active.topic
                key = contest_active.key
                value = contest_active.schema.dump({'contest': new_instance})
                self.service.notify(topic=topic, value=value, key=key)
            elif new_instance.status.name == 'completed':
                topic = contest_completed.topic
                key = contest_completed.key
                value = contest_completed.schema.dump({'contest': new_instance})
                self.service.notify(topic=topic, value=value, key=key)
            elif new_instance.status.name == 'inactive':
                topic = contest_inactive.topic
                key = contest_inactive.key
                value = contest_inactive.schema.dump({'contest': new_instance})
                self.service.notify(topic=topic, value=value, key=key)
        if args.get('avatar'):
            topic = avatar_created.topic
            key = avatar_created.key
            value = avatar_created.schema.dump({'contest': new_instance, 'avatar': args['avatar']})
            self.service.notify(topic=topic, value=value, key=key)
        if prev_instance and prev_instance.get('name') and prev_instance['name'] != new_instance.name:
            topic = name_updated.topic
            key = name_updated.key
            value = name_updated.schema.dump({'contest': new_instance})
            self.service.notify(topic=topic, value=value, key=key)
        if prev_instance and prev_instance.get('start_time') and prev_instance['start_time'] != new_instance.start_time:
            topic = start_time_updated.topic
            key = start_time_updated.key
            value = start_time_updated.schema.dump({'contest': new_instance})
            self.service.notify(topic=topic, value=value, key=key)
