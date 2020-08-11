from ..models import Sport as SportModel
from ..common.db import find, save, init, destroy, count
from ..common.cache import cache, unmemoize


@cache.memoize(timeout=1000)
def count_sport():
    return count(SportModel)


def find_sport(**kwargs):
    return find(model=SportModel, **kwargs)


def init_sport(**kwargs):
    return init(model=SportModel, **kwargs)


def save_sport(sport):
    unmemoize(count_sport)
    return save(instance=sport)


def destroy_sport(sport):
    unmemoize(count_sport)
    return destroy(instance=sport)


def dump_sport(schema, sport, params=None):
    if params:
        for k, v in params.items():
            schema.context[k] = v
    return schema.dump(sport)


def clean_sport(schema, sport, **kwargs):
    return schema.load(sport, **kwargs)
