FROM dockerhub.tax.service.gov.uk/grafana/carbon-relay-ng:1.5.18

COPY templates/carbon-relay-ng.ini /conf/carbon-relay-ng.ini
