# Stage 1: Build
FROM python:3.12-slim-bullseye AS build

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv
RUN python3 -m venv .venv
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

# Stage 2: Run
FROM python:3.12-slim-bullseye

WORKDIR /app

COPY --from=build /app/.venv ./.venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

COPY . /app

# Don't produce .pyc files
ENV PYTHONUNBUFFERED 1    
# Don't buffer stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app

EXPOSE 8080