#!/bin/sh

. ~/.bashrc

pip install -e .

if [ "$DATABASE" = "contest" ]; then
  echo "Waiting for contest..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

manage run -h 0.0.0.0