FROM python:3.11

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY . /fastapi_app

RUN pip install --no-cache -r requirements.txt

RUN sleep 3

RUN alembic upgrade head

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000