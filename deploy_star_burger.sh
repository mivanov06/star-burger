#!/bin/bash

set -e

cd /opt/star-burger/

git pull
source venv/bin/activate

pip install -r requirements.txt

npm ci --dev --prefix /opt/star-burger
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput
systemctl restart star-burger.target
systemctl reload nginx

access_token=$ROLLBAR_TOKEN
commit_hash=$(git rev-parse --verify HEAD)
curl -X POST https://api.rollbar.com/api/1/deploy/ \
     -H "Content-Type: application/json" \
     -H "X-Rollbar-Access-Token: $access_token" \
     -d '{
           "environment": "production",
           "revision": "'"$commit_hash"'",
           "rollbar_name": "mivanov06",
           "local_username": "mivanov06"
           "comment": "new deploy",
           "status": "succeeded"
         }'

echo "Deploy has successefully finished"
