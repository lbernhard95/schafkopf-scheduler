# Base image with Python 3.12
FROM --platform=linux/amd64 python:3.12-slim AS base

WORKDIR /app
USER root
# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN apt-get update && apt-get install -y wget gnupg && \
    wget -O google-key.gpg https://dl.google.com/linux/linux_signing_key.pub && \
    install -o root -g root -m 644 google-key.gpg /usr/share/keyrings/google-linux-signing-keyring.gpg && \
    sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/* google-key.gpg

# Install ChromeDriver
ARG CHROMEDRIVER_VERSION=latest
RUN if [ "$CHROMEDRIVER_VERSION" = "latest" ]; then \
      CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE); \
    fi && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME="/opt/poetry"
ENV PYTHONPATH="/app"
ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN pip3 install poetry==1.8.4

COPY pyproject.toml /app/
COPY poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-root --with beachbooker
COPY core core
COPY beachbooker beachbooker

CMD ["poetry", "run", "python3", "beachbooker/main.py"]

FROM base as local
COPY .env .env
