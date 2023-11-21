FROM ${DOCKERHUB}grafana/carbon-relay-ng

COPY start.sh /start.sh
RUN chmod +x /start.sh

COPY templates/carbon-relay-ng.ini /conf/carbon-relay-ng.ini


#ENTRYPOINT ["/start.sh"]

#CMD ["/start.sh"]
