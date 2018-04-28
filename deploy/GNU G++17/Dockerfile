FROM registry.docker-cn.com/library/gcc:7.3.0
RUN groupadd -g 6666 judge_group                   \
    && useradd -u 6666 -d /home -g 6666 judge_user \
    && chmod -R 700 /opt                           \
    && chmod -R 700 /etc
