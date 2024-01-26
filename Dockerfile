FROM python:slim-bookworm
EXPOSE 80

COPY requirements.txt .
RUN python3 -m ensurepip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Change this if you want some other WSGI
RUN pip3 install gunicorn

RUN mkdir /App
COPY pyteamquiz /App/pyteamquiz

WORKDIR /App

RUN adduser --system --no-create-home herbert
USER herbert

# Change this if you want an other WSGI, or increase the number of workers
ENTRYPOINT gunicorn -w 3 -b 0.0.0.0:8000 pyteamquiz.main:app