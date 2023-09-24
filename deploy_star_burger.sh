#!/bin/bash

set -e

git -C /opt/star-burger pull
/opt/star-burger/venv/bin/pip install -r /opt/star-burger/requirements.txt
/opt/star-burger/venv/bin/python3.10 /opt/star-burger/manage.py makemigrations --dry-run --check
npm ci --dev --prefix /opt/star-burger
/opt/star-burger/venv/bin/python3.10 /opt/star-burger/manage.py collectstatic --noinput
/opt/star-burger/venv/bin/python3.10 /opt/star-burger/manage.py migrate --noinput
systemctl restart star-burger.target
systemctl reload nginx
http POST https://api.rollbar.com/api/1/deploy X-Rollbar-Access-Token:$ROLLBAR_TOKEN environment=$ROLLBAR_ENV revision=$(git rev-parse --verify HEAD) rollbar_username=mivanov06 comment="new deploy" status=succeeded
echo "Deploy has successefully finished"

