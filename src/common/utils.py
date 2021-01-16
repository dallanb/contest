import base64
import uuid as UUID
import datetime
from io import BytesIO
from time import time

from rfc3339 import rfc3339

from .. import app


def generate_hash(items):
    frozen = frozenset(items)
    return hash(frozen)


def time_now():
    return int(time() * 1000.0)


def add_years(t, years=0):
    return t + 31104000000 * years


def generate_uuid():
    return UUID.uuid4()


def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


def file_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1]


def allowed_file(filename):
    return file_extension(filename) in app.config["ALLOWED_EXTENSIONS"]


def get_image_data(file):
    starter = file.find(',')
    image_data = file[starter + 1:]
    image_data = bytes(image_data, encoding="ascii")
    return BytesIO(base64.b64decode(image_data))


def s3_object_name(filename):
    return f"{app.config['S3_FILEPATH']}{filename}"


def request_formatter(request, response, start):
    now = time()
    duration = round(now - start, 2)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt, utc=True)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = [
        ('method', request.method),
        ('path', request.path),
        ('status', response.status_code),
        ('duration', duration),
        ('time', timestamp),
        ('ip', ip),
        ('host', host,),
        ('params', args)
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id))

    parts = []
    for name, value in log_params:
        parts.append(f"{name}={value}")
    return " ".join(parts)