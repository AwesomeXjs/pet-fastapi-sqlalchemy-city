FROM python:3.11

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY . /fastapi_app

RUN pip install --no-cache -r requirements.txt

CMD ["/bin/sh", "/app/start.sh"]