FROM ${DOCKERHUB}grafana/carbon-relay-ng

# Install packages required by Fargate to enable AWS ECS Exec:
RUN apk add coreutils util-linux && apk cache clean

COPY templates/carbon-relay-ng.ini /conf/carbon-relay-ng.ini
