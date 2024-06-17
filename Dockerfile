FROM python:3.11-slim

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt /fastapi_app

RUN pip install -r /fastapi_app/requirements.txt

COPY . /fastapi_app

RUN python -m alembic upgrade head

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000