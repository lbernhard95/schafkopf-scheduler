FROM --platform=linux/amd64 python:3.12-slim
WORKDIR /app

# https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-clients
RUN pip install awslambdaric

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME="/opt/poetry"
ENV PYTHONPATH="/app"

RUN pip install poetry==1.8.4

COPY pyproject.toml /app/
COPY poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY scheduler scheduler
COPY lambda_handler.py lambda_handler.py
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "lambda_handler.lambda_handler" ]
