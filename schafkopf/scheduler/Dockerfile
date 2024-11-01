FROM --platform=linux/amd64 python:3.12
WORKDIR /app

# https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-clients
RUN pip install awslambdaric

# Install required packages and generate locale
RUN apt-get update && \
    apt-get install -y --no-install-recommends locales && \
    rm -rf /var/lib/apt/lists/* && \
    echo "de_DE.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=de_DE.UTF-8

# Set locale environment variables
ENV LANG=de_DE.UTF-8 \
    LC_ALL=de_DE.UTF-8 \
    LANGUAGE=de_DE.UTF-8

ENV PYTHONPATH="/app"

RUN pip install poetry==1.8.4

COPY pyproject.toml /app/
COPY poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY schafkopf schafkopf
COPY templates templates
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "schafkopf.scheduler.lambda_handler.lambda_handler" ]
