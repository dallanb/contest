import enum


class ContestStatusEnum(enum.Enum):
    pending = 1
    ready = 2
    active = 3
    inactive = 4


class ParticipantStatusEnum(enum.Enum):
    pending = 1
    active = 2
    inactive = 3
