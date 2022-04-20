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
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip-sync /tmp/requirements.txt --pip-args $PIP_OPTS ; \
             else pip-sync /tmp/requirements.txt /tmp/requirements-dev.txt '$PIP_OPTS' ; fi"                                                                                                         
COPY ./star_dust ./app

EXPOSE 8080

CMD ["python","-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]


