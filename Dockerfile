FROM python:3.8.8-buster

COPY api /api
COPY visualstoryteller /visualstoryteller
COPY .env /.env
COPY requirements.txt /requirements.txt
COPY key_lewagon_project.json /key_lewagon_project.json

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN echo 'GOOGLE_APPLICATION_CREDENTIALS=/key_lewagon_project.json' >> .env
RUN python -m spacy download en_core_web_sm

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
