#!/bin/bash
K8S_VERSION=${K8S_VERSION:=0.16.2}
K8S_BIN_DIR=${K8S_BIN_DIR:=/opt/bin}


mkdir -p ${K8S_BIN_DIR}

wget -N -P ${K8S_BIN_DIR} https://storage.googleapis.com/kubernetes-release/release/v${K8S_VERSION}/bin/linux/amd64/kube-apiserver
wget -N -P ${K8S_BIN_DIR} https://storage.googleapis.com/kubernetes-release/release/v${K8S_VERSION}/bin/linux/amd64/kube-controller-manager
wget -N -P ${K8S_BIN_DIR} https://storage.googleapis.com/kubernetes-release/release/v${K8S_VERSION}/bin/linux/amd64/kube-scheduler
wget -N -P ${K8S_BIN_DIR} https://storage.googleapis.com/kubernetes-release/release/v${K8S_VERSION}/bin/linux/amd64/kube-proxy
wget -N -P ${K8S_BIN_DIR} https://storage.googleapis.com/kubernetes-release/release/v${K8S_VERSION}/bin/linux/amd64/kubelet
wget -N -P ${K8S_BIN_DIR} https://storage.googleapis.com/kubernetes-release/release/v${K8S_VERSION}/bin/linux/amd64/kubectl

chmod +x ${K8S_BIN_DIR}/kube*
