# Build context must contain the already-built wheel in dist/.
FROM python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df

COPY dist/*.whl /tmp/wheels/

RUN python -m pip --isolated install --no-cache-dir --no-index --no-deps /tmp/wheels/*.whl \
    && rm -rf /tmp/wheels \
    && useradd --create-home --uid 10001 soupcheck

WORKDIR /home/soupcheck
USER soupcheck

ENTRYPOINT ["soupcheck"]
CMD ["report"]
