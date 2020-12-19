#!/bin/sh

docker exec -it contest bash -c "python manage.py reset"
docker exec -it contest bash -c "python manage.py init"