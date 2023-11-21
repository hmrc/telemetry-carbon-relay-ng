
# telemetry-carbon-relay-ng

This is a placeholder README.md for a new repository

### License

This code is open source software licensed under the [Apache 2.0 License]("http://www.apache.org/licenses/LICENSE-2.0.html").

# Running Tests with Docker Compose

Before running the tests, ensure that you have Docker Compose installed and the required containers are built and running.

## Docker Compose Commands

### Build the Docker Container

```bash
docker-compose build

### Start the Docker Container
docker-compose up

### Check Running Container
docker ps
```

### Test Scenarios
Now that the Docker containers are running, proceed to run the test scenarios outlined below.

Test 1: Invalidation Scenario
  1. Navigate to the monitoring Documentation https://github.com/grafana/carbon-relay-ng/blob/master/docs/monitoring.md
  2. Click on the link that's on the first bullet point to get to the performance page
  3. To start the invalid test send a data point to the Carbon server: ```echo "tax.test `date +%s`" | nc -w0 localhost 2003```
  4. Navigate back to the performance page and hit refresh and you should see Err.type_is_invalid": 1

Test 2: Blocking Scenario
  1. Choose a block path to test the blocklist functionality. This can be found in templates/carbon-relay-ng.ini
  2. Send a metric to the Carbon server for the chosen block path: ```echo "tax.test 10 `date +%s`" | nc -w0 localhost 2003```
  3. Navigate back to the performance page and hit refresh and you should see Metric.direction_is_blocklist: 1

Test 3: Successful Scenario
  1. Run the following command to list all running containers and copy the ID of the ClickHouse container: ```docker ps``` 
  2. Enter interactive mode for the ClickHouse container: ```docker exec -it <Container_ID> clickhouse-client```
  3. In the ClickHouse interactive mode, run the following SQL query to check if the ClickHouse container is working:``` SELECT top 5 * FROM graphite.graphite```
  4. Ensure that you see relevant data.
  5. Send a metric to the Carbon ClickHouse setup: ```echo "test.test 5 `date +%s`" | nc -w0 localhost 2003```
  5. Confirm that the metrics you sent are reflected in the ClickHouse database: ```select top 5 * from graphite.graphite where Path = 'test.test'```

### Stop and Remove the Docker Containers:
```docker-compose down```

### Testing complete!!!










