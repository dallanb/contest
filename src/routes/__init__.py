from .v1 import AvatarsAPI
from .v1 import ContestsAPI, ContestsListAPI, ContestsListCalendarAPI, ContestsMaterializedAPI, ContestsMaterializedListAPI
from .v1 import ParticipantsAPI, ParticipantsMemberAPI, ParticipantsListAPI
from .v1 import PingAPI
from .. import api

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])

# Contests
api.add_resource(ContestsMaterializedAPI, '/contests/materialized/<uuid:uuid>', endpoint="contest_materialized")
api.add_resource(ContestsMaterializedListAPI, '/contests/materialized', endpoint="contests_materialized")
api.add_resource(ContestsAPI, '/contests/<uuid:uuid>', endpoint="contest")
api.add_resource(ContestsListAPI, '/contests', endpoint="contests")
api.add_resource(ContestsListCalendarAPI, '/contests/calendar', endpoint="contests_calendar")
# Avatars
api.add_resource(AvatarsAPI, '/contests/<uuid>/avatars', endpoint="avatar")

# Participants
api.add_resource(ParticipantsAPI, '/participants/<uuid:uuid>', endpoint="participant")
api.add_resource(ParticipantsMemberAPI, '/contests/<uuid:contest_uuid>/participants/member/<uuid:member_uuid>',
                 endpoint="participant_member")
api.add_resource(ParticipantsListAPI, '/contests/<uuid:contest_uuid>/participants', '/participants',
                 endpoint="participants")
