# ========================================
# =               Warning!               =
# ========================================
# This is Github Action docker-based image.
# It is not intended for local development!
#
# It can still be used as a raw image for your own containers.
# See `action.yml` in case you want to learn more about Github Actions.
# See it live:
# https://github.com/wemake-services/docker-image-size-limit/actions
#
# This image is also available on Dockerhub:
# https://hub.docker.com/r/wemakeservices/docker-image-size-limit

FROM python:3.12.6-alpine

LABEL maintainer="mail@sobolevn.me"
LABEL vendor="wemake.services"

# Our own tool:
ENV DISL_VERSION='2.1.0'

RUN apk add --no-cache bash docker
RUN pip3 install "docker-image-size-limit==$DISL_VERSION"

COPY ./scripts/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
