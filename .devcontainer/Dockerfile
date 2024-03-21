FROM python:3.12-slim-bullseye AS python

FROM python as debian
ARG DEBIAN_FRONTEND=noninteractive
ARG PROJECT_NAME=project

RUN apt-get update -y && \
    apt-get upgrade -y

RUN apt-get install -y --no-install-recommends \
    bzip2 \
    gcc \
    g++ \
    make \
    git \
    wget \
    curl

RUN apt-get install -y --no-install-recommends \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv

RUN apt-get autoremove -y && \
    apt-get autoclean -y

RUN useradd -ms /bin/bash vscode

USER vscode
WORKDIR /home/vscode


FROM debian as poetry

ENV PATH="/home/vscode/.local/bin:${PATH}"

ARG PYTHON_VIRTUALENV_HOME=/home/vscode/project-py-env \
    POETRY_VERSION=1.8.2

ENV POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=true

RUN python3 -m venv ${PYTHON_VIRTUALENV_HOME} && \
    $PYTHON_VIRTUALENV_HOME/bin/pip install --upgrade pip wheel && \
    $PYTHON_VIRTUALENV_HOME/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="$PYTHON_VIRTUALENV_HOME/bin:$PATH" \
    VIRTUAL_ENV=$PYTHON_VIRTUALENV_HOME

RUN poetry completions bash >> /home/vscode/.bash_completion && \
    echo "export PATH=$PYTHON_VIRTUALENV_HOME/bin:$PATH" >> ~/.bashrc


FROM poetry as project-dev

COPY --chown=vscode:vscode pyproject.toml poetry.lock* ./

RUN poetry install --no-root --with dev --with docs

WORKDIR /workspaces/${PROJECT_NAME}

CMD ["/bin/bash"]
