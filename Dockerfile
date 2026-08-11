ARG CARBON_RELAY_NG_VERSION
FROM dockerhub.tax.service.gov.uk/grafana/carbon-relay-ng:${CARBON_RELAY_NG_VERSION:-1.5.18}

COPY templates/carbon-relay-ng.ini /conf/carbon-relay-ng.ini
