FROM python:3.9-slim as backend

ENV PYTHONBUFFERED=1

RUN apt-get -y update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade --no-cache-dir \
    setuptools \
    wheel \
    pip-tools

RUN useradd --create-home staruser
WORKDIR /home/star-dust
USER staruser

COPY requirements.txt requirements-dev.txt /tmp/

ARG INSTALL_DEV=true
ARG PIP_OPTS="'--no-cache-dir --no-deps'"
RUN bash -c "if [ $INSTALL_DEV == 'false' ] ; then pip-sync /tmp/requirements.txt --pip-args $PIP_OPTS ; \
             else pip-sync /tmp/requirements.txt /tmp/requirements-dev.txt --pip-args $PIP_OPTS ; fi"

COPY ./star_dust ./star_dust
COPY ./alembic ./alembic
COPY alembic.ini docker-entrypoint.sh ./
ENV PATH "$PATH:/home/staruser/.local/bin"

EXPOSE 8080

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh", "--"]

CMD ["python","-m", "uvicorn", "star_dust.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
