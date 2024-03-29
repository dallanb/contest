from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_json import mutable_json_type
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types import TSVectorType

from ... import db
from ...common.utils import camel_to_snake, time_now


class ContestMaterialized(db.Model):
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)

    uuid = db.Column(UUIDType(binary=False), primary_key=True, unique=True, nullable=False)
    ctime = db.Column(db.BigInteger, default=time_now)
    mtime = db.Column(db.BigInteger, onupdate=time_now)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    start_time = db.Column(db.BigInteger, nullable=False)
    avatar = db.Column(db.String, nullable=True)
    owner = db.Column(UUIDType(binary=False), nullable=False)
    location = db.Column(db.String, nullable=False)
    league = db.Column(UUIDType(binary=False), nullable=True)
    participants = db.Column(mutable_json_type(dbtype=JSONB, nested=True))
    search_vector = db.Column(TSVectorType('name', 'location', weights={'name': 'A', 'location': 'B'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
