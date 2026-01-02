# Envoy rewrite tests

These tests verify the behaviour of the Envoy rewrite rules in `templates/carbon-relay-ng.ini` using a Docker Compose metrics stack.
Metrics are pushed to `carbon-relay-ng` and the resulting path is read from `clickhouse`.

To run:
```
cd ..
pip install -r tests/requirements.txt
docker compose up --detach
pytest
docker compose down
```
