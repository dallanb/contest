from .. import api
from .v1 import PingAPI
from .v1 import ContestsAPI, ContestsListAPI, ContestsMaterializedAPI, ContestsMaterializedListAPI
from .v1 import ParticipantsAPI, ParticipantsUserAPI, ParticipantsListAPI
from .v1 import AvatarsAPI

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])

# Contests
api.add_resource(ContestsMaterializedAPI, '/contests/materialized/<uuid:uuid>', endpoint="contest_materialized")
api.add_resource(ContestsMaterializedListAPI, '/contests/materialized', endpoint="contests_materialized")
api.add_resource(ContestsAPI, '/contests/<uuid:uuid>', endpoint="contest")
api.add_resource(ContestsListAPI, '/contests', endpoint="contests")

# Avatars
api.add_resource(AvatarsAPI, '/contests/<uuid>/avatars', endpoint="avatar")

# Participants
api.add_resource(ParticipantsAPI, '/participants/<uuid:uuid>', endpoint="participant")
api.add_resource(ParticipantsUserAPI, '/contests/<uuid:contest_uuid>/participants/user/<uuid:user_uuid>',
                 endpoint="participant_user")
api.add_resource(ParticipantsListAPI, '/contests/<uuid:uuid>/participants', '/participants', endpoint="participants")
