ARG TWIRL_VERSION
FROM europe-docker.pkg.dev/twirldata/twirl/twirl-base:${TWIRL_VERSION}

COPY bigquery/contracts/contract_embedding/requirements.txt .
RUN --mount=type=cache,target=/home/app/.cache \
    pip install -r requirements.txt

COPY . .

ARG GIT_COMMIT_HASH="unknown"
ENV GIT_COMMIT_HASH=${GIT_COMMIT_HASH}

# set ENV as late as possible, to avoid invalidating Docker cache layers above
ARG ENV
ENV ENV=${ENV}
