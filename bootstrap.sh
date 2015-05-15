#!/bin/bash
NAME_PREFIX=${NAME_PREFIX:=tcore0}
NUM_OF_DROPLETS=${NUM_OF_DROPLETS:=2}
set -x
. environments

for i in `seq $NUM_OF_DROPLETS`; do ./create_droplet.sh $NAME_PREFIX$i; done

# update host list for fabric use
:> allhosts
:> allhosts.priv
:> alldid
for i in `seq $NUM_OF_DROPLETS`; do
    DROPLET_STATUS="new"
    DROPLET_DETAILS=""
    DROPLET_ID=""
    while [ "$DROPLET_STATUS" != "active" ]; do
        sleep 15
        DROPLET_DETAILS=`./get_droplet.sh | jq '.droplets[] | select(.name == '\""$NAME_PREFIX$i"\"')'`
        DROPLET_STATUS=`echo $DROPLET_DETAILS | jq '.status' | sed 's/"//g'`
        DROPLET_ID=`echo $DROPLET_DETAILS | jq '.id'`
    done
    PUBLIC_IP=`echo $DROPLET_DETAILS | jq '.networks.v4 | .[] | select(.type =="public") | .ip_address' | sed 's/"//g'`
    PRIVATE_IP=`echo $DROPLET_DETAILS | jq '.networks.v4 | .[] | select(.type =="private") | .ip_address' | sed 's/"//g'`
    echo $PUBLIC_IP >>allhosts;
    echo $PRIVATE_IP >> allhosts.priv
    echo $DROPLET_ID >> alldid
done

# cleanup known hosts lists
:> ~/.fleetctl/known_hosts
for h in `cat allhosts`; do ssh-keygen -f "$HOME/.ssh/known_hosts" -R $h; done

# wait some time to make sure Droplets internally ready
sleep 120
fab set_hosts deploy_minion
fab -H `head -1 allhosts` deploy_master
fab set_hosts start_minion_services
fab -H `head -1 allhosts` setup_dns
