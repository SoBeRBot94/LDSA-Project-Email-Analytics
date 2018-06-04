#!/usr/local/env python3

# Python Fabric File to Deploy Spark Cluster On SNIC Instances

from fabric.api import *
from fabric.decorators import parallel

env.user = 'ubuntu'
env.key_filename = '/home/SoBeRBot94/University-Files/SEM-2/LDSA/Project/team-15-project.pem'
env.hosts = open('hostfile', 'r').readlines()
env.roledefs = {
    'master':[env.hosts[0]],
    'worker':[env.hosts[1]]
        }

@task
def is_up():
    print("\n \n ----- Checking If The Insatnces Are Up ----- \n \n")
    hosts = env.hosts
    for item in list(hosts):
        local('ping -c 5 %s' % item)

@task
@roles('master')
def set_hostname_in_master():
    print("\n \n ----- Set Hostnames ----- \n \n")
    sudo('hostnamectl set-hostname team-15-instance-master')
    sudo('systemctl restart systemd-hostnamed')
    sudo('echo \'team-15-instance-master\' > /etc/hostname')
    sudo('sed -i \'s/127.0.0.1 localhost.*$/127.0.0.1 localhost team-15-instance-master/\' /etc/hosts')

@task
@roles('master')
def add_hosts():
    print("\n \n ----- Adding Hosts ----- \n \n")
    worker = ''.join(env.hosts[1]).rstrip('\n')
    sudo('echo >> /etc/hosts')
    sudo('echo %s team-15-instance-worker >> /etc/hosts' % worker)

@task
@roles('worker')
def set_hostname_in_worker():
    print("\n \n ----- Set Hostnames ----- \n \n")
    sudo('hostnamectl set-hostname team-15-instance-worker')
    sudo('systemctl restart systemd-hostnamed')
    sudo('echo \'team-15-instance-worker\' > /etc/hostname')
    sudo('sed -i \'s/127.0.0.1 localhost.*$/127.0.0.1 localhost team-15-instance-worker/\' /etc/hosts')

@task
@roles('master')
def generate_ssh_keypairs():
    print("\n \n ----- Generating SSH Keys ----- \n \n")
    run('ssh-keygen -t rsa -P \"\"')

@task
@roles('master')
def ssh_keys_master():
    print("\n \n ----- Adding SSH Keys ----- \n \n")
    run('cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys')
    get('~/.ssh/id_rsa.pub', './id_rsa.pub')

@task
@roles('worker')
def ssh_keys_worker():
    print("\n \n ----- Adding SSH Keys ----- \n \n")
    put('./id_rsa.pub', '~/.ssh/id_rsa.pub')
    run('cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys')

@task
@parallel
def install_updates():
    print("\n \n ----- Installing Updates ----- \n \n")
    sudo('apt-get -y update')

@task
@roles('master')
def install_requisites_in_master():
    print("\n \n ----- Installing Requisites ----- \n \n")
    sudo('apt-get -y install default-jre scala python3 python3-pip supervisor')

@task
@roles('master')
def install_jupyter():
    print("\n \n ----- Install Jupyter ----- \n \n")
    sudo('python3 -m pip install jupyter')

@task
@roles('master')
def setup_jupyter_service():
    print("\n \n ----- Setting up Supervisor Service Configuration For Jupyter ----- \n \n")
    put('./jupyter.conf', '/etc/supervisor/conf.d/jupyter.conf', use_sudo=True)
    sudo('supervisorctl reread')
    sudo('supervisorctl reload')

@task
@roles('worker')
def install_requisites_in_worker():
    print("\n \n ----- Installing Requisites ----- \n \n")
    sudo('apt-get -y install default-jre scala python3 python3-pip')

@task
@parallel
def install_pyspark():
    print("\n \n ----- Installing PySpark ----- \n \n")
    sudo('python3 -m pip install pyspark')

@task
@parallel
def set_java_env():
    print("\n \n ----- Setting Java Environment Variables ----- \n \n")
    sudo('echo >> /etc/profile')
    sudo('echo \'export JAVA_HOME=/usr/lib/jvm/default-java\' >> /etc/profile')
    sudo('echo \'export PATH=$PATH:$JAVA_HOME/bin\' >> /etc/profile')

@task
@parallel
def upgrade_pip():
    print("\n \n ----- Upgrading PIP Version ----- \n \n")
    sudo('python3 -m pip install --upgrade pip')

@task
@parallel
def fetch_spark_tarball():
    print("\n \n ----- Fetching Spark Tar Ball ----- \n \n")
    sudo('wget http://www-eu.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz')

@task
@parallel
def extract_spark_tarball():
    print("\n \n ----- Extract ----- \n \n")
    sudo("tar xvf spark-2.3.0-bin-hadoop2.7.tgz")

@task
@parallel
def setup_spark_env():
    print("\n \n ----- Setting Up Spark Environment & Environment variables ----- \n \n")
    sudo('mv /home/ubuntu/spark-2.3.0-bin-hadoop2.7 /usr/local/spark')
    sudo('chown -R ubuntu:ubuntu /usr/local/spark')
    sudo('echo >> /etc/profile')
    sudo('echo \'export SPARK_HOME=/usr/local/spark\' >> /etc/profile')
    sudo('echo \'export PATH=$PATH:$SPARK_HOME/bin\' >> /etc/profile')

@task
@parallel
def configure_spark():
    print("\n \n ----- Configuring Spark Cluster Nodes ----- \n \n")
    worker = ''.join(env.hosts[1]).rstrip('\n')
    run('cp /usr/local/spark/conf/spark-env.sh.template /usr/local/spark/conf/spark-env.sh')
    run('echo >> /usr/local/spark/conf/spark-env.sh')
    run('echo \'export JAVA_HOME=/usr/lib/jvm/default-java\' >> /usr/local/spark/conf/spark-env.sh')
    run('echo \'export SPARK_WORKER_CORES=6\' >> /usr/local/spark/conf/spark-env.sh')
    run('echo \'%s\' > /usr/local/spark/conf/slaves' % worker)

@task
@roles('master')
def configure_spark_master():
    print("\n \n ----- Configure Spark Master Node ----- \n \n")
    master = run('ifconfig | grep inet\ addr | awk \'FNR ==1 {print $2}\' | cut -d \':\' -f 2')
    run('echo \'export SPARK_MASTER_HOST=%s\' >> /usr/local/spark/conf/spark-env.sh' % master)

@task
def clean_up():
    print("\n \n ----- Cleaning Up Junk ----- \n \n")
    local('rm -rf ./id_rsa.pub ./__pycache__')
