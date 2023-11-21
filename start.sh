#!/bin/bash

sed -i "s/{{CARBON_CLICKHOUSE_HOST_SHARD_1}}/${CARBON_CLICKHOUSE_HOST_SHARD_1}/" /conf/carbon-relay-ng.ini
sed -i "s/{{CARBON_CLICKHOUSE_HOST_SHARD_2}}/${CARBON_CLICKHOUSE_HOST_SHARD_2}/" /conf/carbon-relay-ng.ini
sed -i "s/{{CARBON_CLICKHOUSE_PORT}}/${CARBON_CLICKHOUSE_PORT}/" /conf/carbon-relay-ng.ini


exec ${DOCKERHUB}grafana/carbon-relay-ng