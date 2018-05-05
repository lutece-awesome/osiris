# Osiris-Judge-Core
[![Python](https://img.shields.io/badge/python-3.5.2-orange.svg?style=flat-square)](https://www.python.org/downloads/release/python-352/)
[![License](https://img.shields.io/badge/License-GPLv3-ff69b4.svg?style=flat-square)](https://www.gnu.org/licenses/gpl.html)



Judge core based on Docker.

## Current Support Language

+ GNU G++17
+ Clang 6.0.0
+ GNU GCC 7.3
+ Python 3.6.5
+ Java 10
+ Javascript
+ Go 1.9.2
+ Ruby 2.5.1
+ Rust 1.25.0


## Installation

+ Install submodule
<pre>
    git submodule init
    git submodule update
</pre>

+ Install `docker`
<pre>
    suao apt-get update
    sudo apt-get install docker.io
</pre>

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

## Config
+ Edit util.settings.py
<pre>
    FETCH_SUBMISSION_ADDR = 'Lutece.address'
    FETCH_SUBMISSION_AUTHKEY = 'Lutece.settings.JUDGER_AUTHKEY'
</pre>
+ Edit settings.py
<pre>
    MAX_JUDGE_PROCESS = 'eq the number of CPU cores is better'
</pre>
