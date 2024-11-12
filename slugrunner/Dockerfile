FROM artefacts.tax.service.gov.uk/slugrunner:1.43.0

ENV SLUG_URL https://artefacts.tax.service.gov.uk/artifactory/webstore/slugs/alert-simulator/alert-simulator_0.34.0_0.5.2.tgz
ENV SLUG_SIGNING_KEY_FINGERPRINT 8D039CA6D83E948088C3056BA90DC320C2E69D53

ENTRYPOINT ["/runner/init","start","web"]
