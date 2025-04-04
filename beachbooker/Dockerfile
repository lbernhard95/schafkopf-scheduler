FROM --platform=linux/amd64 selenium/standalone-chrome AS base
WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME="/opt/poetry"
ENV PYTHONPATH="/app"
ENV PIP_BREAK_SYSTEM_PACKAGES=1
USER root
RUN pip3 install poetry==1.8.4

COPY pyproject.toml /app/
COPY poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-root --with beachbooker
COPY core core
COPY beachbooker beachbooker

CMD ["poetry", "run", "python3", "beachbooker/main.py"]

FROM base AS local
COPY .env .env

FROM base AS lambda
RUN pip install awslambdaric

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "beachbooker.core.lambda_handler.handler" ]
