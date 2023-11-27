FROM ${DOCKERHUB}grafana/carbon-relay-ng

COPY init.sh /init.sh
RUN chmod +x /init.sh

COPY templates/carbon-relay-ng.ini /etc/carbon-relay-ng.ini

CMD ["/init.sh"]