# telemetry-carbon-relay-ng

> [!WARNING]
> The tests in `tests/` are not run automatically and do not cover all functionality

# Running Tests with Docker Compose

Before running the tests, ensure that you have Docker Compose installed and the required containers are built and running.

## Table of Contents
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Prerequisites](#prerequisites)
- [Docker Compose Commands](#docker-compose-commands)
  - [Build and run the Docker Containers](#build-and-run-the-docker-containers)
- [Test Scenarios](#test-scenarios)
  - [Test 1: Invalidation Scenario](#test-1-invalidation-scenario)
  - [Test 2: Blocking Scenario](#test-2-blocking-scenario)
  - [Test 3: Successful Scenario](#test-3-successful-scenario)
  - [Clean-up the test artifacts](#clean-up-the-test-artifacts)
- [License](#license)

<!-- END doctoc -->

## Prerequisites

- [mise](https://mise.jdx.dev/) to manage tool versions and integrates with `uv`.
- [uv](https://docs.astral.sh/uv/) to manage Python virtual environments and dependencies.

## Docker Compose Commands

### Build and run the Docker Containers

```shell
# Build the telemetry carbon-relay-ng container image
docker compose build

# Ensure no stale data
docker volume rm telemetry-carbon-relay-ng_clickhouse_data

# Start compose stack
docker compose up --detach

# Check containers are running
docker compose ps
```

## Test Scenarios

The docker compose stack must be running for the following test scenarios outlined below.

### Test 1: Invalidation Scenario

  1. Send an invalid data point to the Carbon server:

     ```shell
     echo "tax.test `date +%s`" | nc -w0 localhost 2003
     ```

  2. Confirm that the Carbon server reports invalid data:

     ```shell
     curl --silent http://localhost:8081/debug/vars2 | grep 'Err.type_is_invalid": 1'
     ```

### Test 2: Blocking Scenario

  1. Choose a block path to test the blocklist functionality (this can be found in [templates/carbon-relay-ng.ini](./templates/carbon-relay-ng.ini)).
  2. Send a metric to the Carbon server for the chosen block path, for example:

     ```shell
     echo "tax.test 10 `date +%s`" | nc -w0 localhost 2003
     ```

  3. Confirm that the Carbon server reports a blocklist:

     ```shell
     curl --silent http://localhost:8081/debug/vars2 | grep 'Metric.direction_is_blocklist": 1'
     ```

### Test 3: Successful Scenario

  1. Run the following command and verfiy five rows are returned:

     ```shell
     docker compose exec clickhouse \
       clickhouse-client -q "SELECT * FROM graphite.graphite ORDER BY Date DESC  LIMIT 5"
     ```

  2. Send a metric to the Carbon ClickHouse setup:

     ```shell
     echo "test.test 5 `date +%s`" | nc -w0 localhost 2003
     ```

  3. Run the following command and verfiy one row is returned:

     ```shell
     docker compose exec clickhouse \
       clickhouse-client -q "SELECT * FROM graphite.graphite where Path = 'test.test'"
     ```

### Clean-up the test artifacts

```shell
docker compose down
docker volume rm telemetry-carbon-relay-ng_clickhouse_data
```

## License

This code is open source software licensed under the [Apache 2.0 License]("http://www.apache.org/licenses/LICENSE-2.0.html").
