#!/bin/bash

# set -e
# chalice local --port=7415 --host=0.0.0.0 && /usr/sbin/nginx -g 'daemon off;'

set -e
python -m scripts.create_first_admin
exec uvicorn main:app --reload --host 0.0.0.0 --port 7415