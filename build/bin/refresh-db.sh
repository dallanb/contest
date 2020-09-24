#!/bin/sh

docker exec -it contest bash -c "python manage.py reset_db"
docker exec -it contest bash -c "python manage.py init"