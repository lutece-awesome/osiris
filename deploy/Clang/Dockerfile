FROM registry.docker-cn.com/library/ubuntu:bionic

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update  \
    && apt-get install -y software-properties-common \
    && apt-get install -y wget \
    && wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - \
    && apt-add-repository "deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-6.0 main" \
    && apt-get update \
    && apt-get install -y clang-6.0 \
    && apt-get remove wget software-properties-common \
    && apt-get remove --purge -y clang-6.0 $(apt-mark showauto) \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -g 6666 judge_group \
    && useradd -u 6666 -d /home -g 6666 judge_user
