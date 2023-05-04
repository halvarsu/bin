#!/bin/bash

NOTEBOOKS=$(jupyter notebook list --jsonlist)
TOKEN=$(echo $NOTEBOOKS | jq --raw-output ".[0].token")
HOSTNAME=$(echo $NOTEBOOKS | jq --raw-output ".[0].hostname")
PORT=$(echo $NOTEBOOKS | jq --raw-output ".[0].port")
curl -sSLG $HOSTNAME:$PORT/api/sessions --data-urlencode "token=$TOKEN"
