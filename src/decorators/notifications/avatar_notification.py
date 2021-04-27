from functools import wraps

from ...notifications import avatar_created, avatar_updated, avatar_deleted


class avatar_notification:
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            prev_instance = {**kwargs.get('instance').__dict__} if kwargs.get('instance') else None
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)
            elif self.operation == 'update':
                self.update(new_instance=new_instance)
            elif self.operation == 'delete':
                self.delete(prev_instance=prev_instance)

            return new_instance

        return wrap

    @staticmethod
    def create(new_instance):
        avatar_created.from_data(avatar=new_instance).notify()

    @staticmethod
    def update(new_instance):
        avatar_updated.from_data(avatar=new_instance).notify()

    @staticmethod
    def delete(prev_instance):
        avatar_deleted.from_data(avatar=prev_instance).notify()
