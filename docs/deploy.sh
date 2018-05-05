#!/bin/bash

echo "do docs deploy"
exit 0

set -e

HOST=yuca.yunity.org

REF=$1

ssh-keyscan -H $HOST >> ~/.ssh/known_hosts

rsync -avz --delete docs-dist/ "deploy@$HOST:karrot-docs/$REF/"

if [ ! -z "$SLACK_WEBHOOK_URL" ]; then
  DEPLOY_ENV="development"
  DEPLOY_EMOJI=":beer:"
  REPO_URL="https://github.com/yunity/karrot-frontend"
  REF_URL="$REPO_URL/tree/$REF"
  COMMIT_URL="$REPO_URL/tree/$COMMIT_SHA"

  COMMIT_MESSAGE=$(git log -1 --pretty="%s - %an")

  DOCBOOK_URL="https://docs.karrot.world"
  ATTACHMENT_TEXT="\n:page_facing_up: <$DOCBOOK_URL|View docs>"

  ATTACHMENT_FOOTER="Using git ref <$REF_URL|$REF>, commit <$COMMIT_URL|$COMMIT_SHA_SHORT> - $COMMIT_MESSAGE"

  payload=$(printf '{
      "channel": "#karrot-git",
      "username": "deploy",
      "text": ":sparkles: Successful deployment of *karrot* to _%s_ %s",
      "attachments": [
        {
          "text": "%s",
          "footer": "%s"
        }
      ]
    }' "$DEPLOY_ENV" "$DEPLOY_EMOJI" "$ATTACHMENT_TEXT" "$ATTACHMENT_FOOTER")

  curl -X POST --data-urlencode "payload=$payload" "$SLACK_WEBHOOK_URL"

fi
