FROM python:3.9-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install Flask gunicorn classy_classification spacy
RUN python -m spacy download en_core_web_sm

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app