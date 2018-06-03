FROM registry.docker-cn.com/library/ubuntu:16.04
RUN apt-get update  \
    && apt-get install -y software-properties-common \
    && apt-get install -y wget \
    && wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - \
    && apt-add-repository "deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-6.0 main" \
    && apt-get update \
    && apt-get install -y clang-6.0 \
    && groupadd -g 6666 judge_group \
    && useradd -u 6666 -d /home -g 6666 judge_user
