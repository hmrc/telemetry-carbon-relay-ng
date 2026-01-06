FROM dockerhub.tax.service.gov.uk/grafana/carbon-relay-ng

COPY templates/carbon-relay-ng.ini /conf/carbon-relay-ng.ini
