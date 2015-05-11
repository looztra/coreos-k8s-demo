from fabric.api import *
from fabric.decorators import task
from fabric.tasks import Task
from fabric.contrib.project import upload_project
from fabric.contrib.files import append

from paramiko import Transport
from socket import getdefaulttimeout, setdefaulttimeout

env.user = 'core'

class SkipIfOfflineTask(Task):
    def __init__(self, func, *args, **kwargs):
        super(SkipIfOfflineTask, self).__init__(*args, **kwargs)
        self.func = func

    def run(self, *args, **kwargs):
        original_timeout = getdefaulttimeout()
        setdefaulttimeout(3)
        try:
            Transport((env.host, int(env.port)))
            return self.func(*args, **kwargs)
        except:
            print "Skipping offline host: " + env.host_string
        setdefaulttimeout(original_timeout)

@task
def get_master_private_ip(private_hostfile='allhosts.priv'):
    """ read and store master private ip for later usage """
    with open(private_hostfile, 'r') as f:
        first_line = f.readline().strip('\r\n')
        env.k8s_master_private_ip = first_line
    print "found k8s_master_private_ip:"+env.k8s_master_private_ip


@task
def enhance_etc_environment():
    """ enhance /etc/environment file with k8s_master_private_ip """
    append('/etc/environment',"K8S_MASTER_PRIVATE_IP="+env.k8s_master_private_ip,use_sudo=True)

@task
def set_hosts(hostfile='allhosts'):
    """ read and set up server list from file """

    remote_servers = []

    file = open(hostfile, 'r')
    for line in file.readlines():
        remote_servers.append(line.strip('\r\n'))

    env.hosts = remote_servers

@task
def deploy_binaries():
    """ deploy pre-built executables """
    sudo('mkdir -p /opt/bin')
    #upload_project(local_dir='./bin', remote_dir='/opt', use_sudo=True)
    put('./scripts/*', '/opt/bin', use_sudo=True, mirror_local_mode=True)
    sudo('chmod +x /opt/bin/get_k8s_binaries.sh')
    sudo('chmod +x /opt/bin/wupiao')
    sudo('/opt/bin/get_k8s_binaries.sh')

@task
def setup_dns():
    """ setup dns stuff: skydns + kube2sky """
    sudo('mkdir -p /etc/dns_token')
    sudo('mkdir -p /etc/kubernetes/dns')
    put('./static/dns/*', '/etc/kubernetes/dns/', use_sudo=True, mirror_local_mode=True)
    with settings(warn_only=True):
        sudo('kubectl create -f /etc/kubernetes/dns/token-system-dns.yaml')
    sudo('kubectl create -f /etc/kubernetes/dns/skydns-rc.yaml')
    sudo('kubectl create -f /etc/kubernetes/dns/skydns-svc.yaml')

@task
def deploy_common_services():
    """ deploy common service files """
    put('./minion/*', '/etc/systemd/system', use_sudo=True)

    sudo('systemctl enable docker.service')
    sudo('systemctl enable /etc/systemd/system/kube-proxy.service')
    sudo('systemctl enable /etc/systemd/system/kubelet.service')

    sudo('systemctl daemon-reload')

    sudo('systemctl start flanneld')
    sudo('systemctl start docker')


@task
def start_minion_services():
    """ start minion services """
    sudo('systemctl start kube-proxy')
    sudo('systemctl start kubelet')

@task(task_class=SkipIfOfflineTask)
def deploy_minion():
    """ deploy minion node """
    get_master_private_ip()
    enhance_etc_environment()
    deploy_binaries()
    deploy_common_services()

@task(task_class=SkipIfOfflineTask)
def deploy_master():
    """ deploy master node """
    put('./master/*', '/etc/systemd/system', use_sudo=True)
    sudo('/opt/bin/substitute_machines.sh /etc/systemd/system/kube-controller-manager.service')

    sudo('systemctl enable /etc/systemd/system/kube-apiserver.service')
    sudo('systemctl enable /etc/systemd/system/kube-controller-manager.service')
    sudo('systemctl enable /etc/systemd/system/kube-scheduler.service')

    sudo('systemctl daemon-reload')

    sudo('systemctl start kube-apiserver')
    sudo('systemctl start kube-controller-manager')
    sudo('systemctl start kube-scheduler')
