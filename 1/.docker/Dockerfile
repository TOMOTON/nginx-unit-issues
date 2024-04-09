ARG ALPINE_VERSION=edge

#---
FROM alpine:${ALPINE_VERSION} as builder
ENV PYTHONUNBUFFERED 1
RUN apk add --no-cache \
        libxslt-dev \
        libffi-dev \
        libgit2-dev\
        openssl1.1-compat-dev \
        cargo \
        python3-dev \
        py3-pip

WORKDIR /wheels
COPY ./requirements*.txt /wheels/
RUN pip install -U wheel \
        && pip wheel -r ./requirements.txt

#---
FROM alpine:${ALPINE_VERSION}
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache \
        bash \
        curl \
        py3-pip \
        unit \
        unit-python3

COPY --from=builder /wheels /wheels
COPY .unit/docker-entrypoint.d /docker-entrypoint.d
COPY .unit/docker-entrypoint.sh /usr/local/bin/
RUN pip install -r /wheels/requirements.txt \
                -f /wheels \
        && rm -rf /wheels \
        && rm -rf /root/.cache/pip/* \
        && addgroup -g 2000 vcap \
        && adduser -D -u 2000 -G vcap vcap \
        && mkdir -p /home/vcap \
        && chown vcap:vcap /home/vcap

USER vcap
ENV USER vcap
ENV HOME /home/vcap

WORKDIR /home/vcap
COPY --chown=vcap:vcap . /home/vcap

USER root

STOPSIGNAL SIGTERM

RUN ln -sf /dev/stdout /var/log/unit.log \
        && chmod +x /usr/local/bin/docker-entrypoint.sh \
        && ln -sf /tmp /usr/tmp

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]

ENV PATH /home/vcap/.local/bin:$PATH
