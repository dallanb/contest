#!/bin/bash

ssh -i /home/dallanbhatti/.ssh/github super_dallan@mega <<EOF
  docker exec contest_db pg_dump -c -U "$1" contest > contest.sql
EOF
rsync -chavzP --stats --remove-source-files super_dallan@mega:/home/super_dallan/contest.sql "$HUNCHO_DIR"/services/contest/contest.sql

docker exec -i contest_db psql -U "$1" contest <"$HUNCHO_DIR"/services/contest/contest.sql
