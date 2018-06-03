# Osiris-Judge-Core
[![Python](https://img.shields.io/badge/python-3.5.4-orange.svg?style=flat-square)](https://www.python.org/downloads/release/python-354/)
[![License](https://img.shields.io/badge/License-GPLv3-ff69b4.svg?style=flat-square)](https://www.gnu.org/licenses/gpl.html)



Judge core based on Celery and Docker.

## Current Support Language

+ GNU G++17
+ Clang 6.0.0
+ GNU GCC 7.3
+ Python 3.6.5
+ Java 10(OpenJDK Runtime Environment (build 10.0.1+10-Debian-4)
+ Go 1.10.2
+ Ruby 2.5.1
+ Rust 1.25.0

## Coming Language

+ Javascript
+ Matlab

## Installation

+ Install submodule
<pre>
    git submodule init
    git submodule update
</pre>

+ Install [`docker-ce`](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce-1)

+ Install requirements
<pre>
    pip3 install -r requirements/requirements.txt
</pre>

+ Install judger's image
<pre>
    cd deploy && python3 deploy.py
</pre>

+ Install checker from testlib
<pre>
    cd checker && python3 install.py
</pre>

+ Compile core
<pre>
    cd core && gcc -o core.bin core.c -O2 -lpthread
</pre>

+ Install rabbitmq-server

<pre>
    sudo apt-get update
    sudo apt-get install rabbitmq-server
    sudo systemctl enable rabbitmq-server
    sudo systemctl start rabbitmq-server
    sudo systemctl status rabbitmq-server
</pre>

## Config

+ Edit util/settings.py
<pre>
    FETCH_DATA_ADDR = Lutece.address
    FETCH_DATA_AUTHKEY = Lutece.data_server.authkey
    ! You may pay attention to http or https
</pre>

+ Edit settings.py
<pre>
    MAX_JUDGE_PROCESS = the number of worker process
</pre>

+ Edit celeryconfig.py
<pre>
    cp celeryconfig.py.template celeryconfig.py
    rabbitmq_ip = Lutece.address
    rabbitmq_pwd = Lutece.rabbitmq.judge_user.password
</pre>

## Run:
<pre>
    sh run_worker.sh
</pre>

## Close
<pre>
    Press ctrl + c close worker
</pre>