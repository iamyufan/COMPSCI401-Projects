# syntax=docker/dockerfile:1

FROM python:3.7-slim

WORKDIR ./

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY app.py ./

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]