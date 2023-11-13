
# telemetry-carbon-relay-ng

This is a placeholder README.md for a new repository

### License

This code is open source software licensed under the [Apache 2.0 License]("http://www.apache.org/licenses/LICENSE-2.0.html").

### Running Tests

# Test 1: Invalidation Scenario
- To test if the configuration is invalid navigate to https://github.com/grafana/carbon-relay-ng/blob/master/docs/monitoring.md and click on the first bullet point 
- Then send data point to the Carbon server example ```echo "tax.test  `date +%s`" | nc -w0 localhost 2003 ```
- This should give you invalid test 

# Test 2: Blocking Scenario
- To tests if the blocklist works pick a block path and send metrics to carbon server for example ```echo "tax.test 10 `date +%s`" | nc -w0 localhost 2003 ```

# Test 3: Successful Scenario
- To test if your metrics are being sent to clickhouse 
- Run < docker ps > to get list of the container 
- Copy your clickhouse container ID and run < docker exec -it < Container ID > clickhouse-client > to get into interactive mode 
- Run < Run select top 5 * from graphite.graphite > to see if your container is working 
- Then send metrics to see if the carbon clickhouse is recieving metrics. example ```echo "test.test 5 `date +%s`" | nc -w0 localhost 2003```
- Using clickhouse client run  ```select top 5 * from graphite.graphite where Path = 'test.test' ``` This should show you the metrics you have sent into clickhouse