from .. import api
from .v1 import PingAPI
from .v1 import ContestsAPI, ContestsListAPI
from .v1 import ParticipantsAPI, ParticipantsListAPI

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])

# Contests
api.add_resource(ContestsAPI, '/contests/<uuid:uuid>', endpoint="contest")
api.add_resource(ContestsListAPI, '/contests', endpoint="contests")

# Participants
api.add_resource(ParticipantsAPI, '/participants/<uuid:uuid>', endpoint="participant")
api.add_resource(ParticipantsListAPI, '/contests/<uuid:uuid>/participants', '/participants', endpoint="participants")
