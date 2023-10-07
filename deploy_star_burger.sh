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
echo "reload nginx"

rollbar_token=$ROLLBAR_TOKEN
rollbar_env=$ROLLBAR_ENV
commit_hash=$(git rev-parse --verify HEAD)

curl --request POST --url https://api.rollbar.com/api/1/deploy \
     --header 'X-Rollbar-Access-Token: $ROLLBAR_TOKEN' \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
            {
              "environment": "$ROLLBAR_ENV",
              "revision": "$commit_hash",
              "rollbar_username": "mivanov06",
              "local_username": "mivanov06",
              "comment": "new deploy",
              "status": "succeeded"
            }
            '

echo "Deploy has successefully finished"

