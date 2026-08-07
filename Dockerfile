FROM dockerhub.tax.service.gov.uk/grafana/carbon-relay-ng:1.5.17

COPY templates/carbon-relay-ng.ini /conf/carbon-relay-ng.ini
