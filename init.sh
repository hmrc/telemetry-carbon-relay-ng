#!/bin/bash

sed -e "s|{{CARBON_CLICKHOUSE_HOST_SHARD_1}}|${CARBON_CLICKHOUSE_HOST_SHARD_1}|" \
    -e "s|{{CARBON_CLICKHOUSE_HOST_SHARD_2}}|${CARBON_CLICKHOUSE_HOST_SHARD_2}|" \
    templates/carbon-relay-ng.ini > conf/carbon-relay-ng.ini


exec ${DOCKERHUB}grafana/carbon-relay-ng
