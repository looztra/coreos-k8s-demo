#!/bin/bash

for DID in `cat alldid`
do
  echo "Deleting droplet with id $DID"
  curl -X DELETE -H 'Content-Type: application/json' -H "Authorization: Bearer $DIGITALOCEAN_ACCESS_TOKEN" "https://api.digitalocean.com/v2/droplets/$DID"
done
