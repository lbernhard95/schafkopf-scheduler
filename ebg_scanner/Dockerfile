FROM --platform=linux/amd64 python:3.12
WORKDIR /app

# https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-clients
RUN pip install awslambdaric

ENV PYTHONPATH="/app"

RUN pip install poetry==1.8.4

COPY pyproject.toml /app/
COPY poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY ebg_scanner ebg_scanner
COPY core core
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "ebg_scanner.lambda_handler.lambda_handler" ]
