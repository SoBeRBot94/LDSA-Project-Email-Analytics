#!/usr/local/env python3

# Python Fabric File to Deploy Spark Cluster On SNIC Instances

from fabric.api import *
from fabric.decorators import parallel

env.user = 'ubuntu'
env.key_filename = '/home/SoBeRBot94/University-Files/SEM-2/LDSA/Project/team-15-instance-key.pem'
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

@task
@roles('worker')
def install_requisites_in_worker():
    print("\n \n ----- Installing Requisites ----- \n \n")
    sudo('apt-get -y install default-jre scala python3 python3-pip')

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

