from functools import wraps


class contest_notification:
    def __init__(self, operation):
        self.operation = operation
        self.topic = 'contests'
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
        key = 'contest_created'
        value = {
            'uuid': str(new_instance.uuid),
            'league_uuid': str(new_instance.league_uuid) if new_instance.league_uuid else None,
            'owner_uuid': str(new_instance.owner_uuid)}
        self.service.notify(topic=self.topic, value=value, key=key, )

    def update(self, prev_instance, new_instance, args):
        if prev_instance and prev_instance.get('status') and prev_instance['status'].name != new_instance.status.name:
            key = f'contest_{new_instance.status.name}'
            value = {
                'uuid': str(new_instance.uuid),
                'owner_uuid': str(new_instance.owner_uuid),
                'league_uuid': str(new_instance.league_uuid) if new_instance.league_uuid else None,
                'message': self.generate_message(key=key, contest=new_instance)
            }
            self.service.notify(topic=self.topic, value=value, key=key)
        if args.get('avatar'):
            key = 'avatar_created'
            value = {
                'uuid': str(args['avatar'].uuid),
                'contest_uuid': str(new_instance.uuid),
                'league_uuid': str(new_instance.league_uuid) if new_instance.league_uuid else None,
                's3_filename': str(args['avatar'].s3_filename)
            }
            self.service.notify(topic=self.topic, value=value, key=key)
        if prev_instance and prev_instance.get('name') and prev_instance['name'] != new_instance.name:
            key = 'name_updated'
            value = {
                'uuid': str(new_instance.uuid),
                'league_uuid': str(new_instance.league_uuid) if new_instance.league_uuid else None,
                'name': new_instance.name
            }
            self.service.notify(topic=self.topic, value=value, key=key)
        if prev_instance and prev_instance.get('start_time') and prev_instance['start_time'] != new_instance.start_time:
            key = 'start_time_updated'
            value = {
                'uuid': str(new_instance.uuid),
                'league_uuid': str(new_instance.league_uuid) if new_instance.league_uuid else None,
                'start_time': new_instance.start_time
            }
            self.service.notify(topic=self.topic, value=value, key=key)

    @staticmethod
    def generate_message(key, **kwargs):
        if key == 'contest_ready':
            contest = kwargs.get('contest')
            return f"{contest.name} is ready"
        elif key == 'contest_active':
            contest = kwargs.get('contest')
            return f"{contest.name} is active"
        else:
            return ''
