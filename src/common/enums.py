import enum


class ContestStatusEnum(enum.Enum):
    pending = 1
    ready = 2
    active = 3
    completed = 4
    inactive = 5


class ParticipantStatusEnum(enum.Enum):
    pending = 1
    active = 2
    completed = 3
    inactive = 4
