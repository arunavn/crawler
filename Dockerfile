FROM ubuntu:latest
RUN apt-get update && apt-get -y install python3.8 python3.8-dev && apt-get -y install python3-pip
WORKDIR /etc/app
COPY ./apps/ apps
COPY ./crawler/ crawler
COPY ./manage.py ./manage.py
WORKDIR /etc/app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
EXPOSE  8000
ENTRYPOINT [ "gunicorn" ]
CMD [ "--bind 0.0.0.0:8000", "crawler.wsgi" ]