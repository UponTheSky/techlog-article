FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.production.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./techlog_article /code/techlog_article

COPY ./main.py /code/

CMD ["python", "./main.py"]
