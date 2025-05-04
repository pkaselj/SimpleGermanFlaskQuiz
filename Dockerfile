FROM python:3.13.3-alpine

WORKDIR /simple_german_quiz

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY ./app/ app/
COPY ./data/ data/

ENV FLASK_APP=app/app.py
ENV FLASK_QUIZ_DATA_DIR=/simple_german_quiz/data

EXPOSE 5000
ENTRYPOINT gunicorn --access-logfile=- --chdir /simple_german_quiz/app -b localhost:5000 -w 4 app:app