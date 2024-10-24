FROM ${DOCKERHUB}grafana/carbon-relay-ng

RUN apk add coreutils util-linux && apk cache clean

COPY templates/carbon-relay-ng.ini /conf/carbon-relay-ng.ini
