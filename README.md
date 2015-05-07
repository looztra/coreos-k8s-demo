# Quick Start

## changes

- coreos > 554 comes bundled with flannel (so no more flannel build step and a flanneld drop-in instead of a full unit)
- works with kubernetes version 0.16.2
- kubernets binaries are downloaded on the remote hosts (no local compilation needed)

## environment dependencies

Scripts in this repo use [jq](stedolan.github.io/jq/) to parse JSON data from
Digital Ocean's API response. If not yet installed, please run following
command.

    $ cd ~/bin && wget http://stedolan.github.io/jq/download/linux64/jq && chmod a+x jq

Also using [Fabric](http://www.fabfile.org/) for Kubernetes deployment.

    $ sudo pip install Fabric

## build binaries

This step is deprecated, flannel and kubernetes will be downloaded on the remote hosts

## start CoreOS cluster and deploy Kubernetes

Run following bootstrap.sh script will create 2 nodes cluster by default on
Digital Ocean and configure systemd
services for Kubernetes. Use following env variable to control number of nodes
to be created.

    $ export NUM_OF_DROPLETS=<number of nodes>

- ssh keys id need to be setup through the DO_SSH_KEY_IDS env var
- Region, and size can also be configured through env vars (DROPLET_SIZE and DROPLET_REGION).  The number of
nodes can be configured in bootstrap.sh, and the first node will
be named as tcore01 and selected as master by default.

    $ cd coreos-k8s-demo
    $ DO_TOKEN=<your token> DO_SSH_KEY_IDS=<id1>,<id2> DROPLET_SIZE=2gb DROPLET_REGION=ams3 NUM_OF_DROPLETS=3 ./bootstrap.sh

## ready to use

Log into master server and verify minion list

    $ kubectl get minions
