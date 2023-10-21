FROM python:3.11

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get install libpq-dev -y \
    && apt-get clean

# use built-in pip to access poetry
RUN pip install poetry

WORKDIR /app/

COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN poetry config virtualenvs.create false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY . /app
ENV PYTHONPATH=/app

EXPOSE 81
RUN cp .env.exemple .env
# CMD poetry run uvicorn app.main:app --port 81
RUN poe _bash_completion >> /root/.bashrc
