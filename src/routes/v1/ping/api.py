from flask import g
from flask_restful import marshal_with
from ..base import Base
from ....common import MessageResponse


class PingAPI(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(MessageResponse.marshallable())
    def get(self):
        g.producer.send(topic='dallan', value=b'pong')
        return MessageResponse(message='pong')
