FROM ubuntu:latest
RUN apt-get update && apt-get -y install python3.8 python3.8-dev && apt-get -y install python3-pip && apt-get -y install wget
WORKDIR /etc
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux32.tar.gz
RUN tar -xvzf geckodriver-v0.29.1-linux32.tar.gz
RUN mv ./geckodriver  /usr/local/bin
WORKDIR /usr/local/bin
RUN chmod +x ././geckodriver
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
ENTRYPOINT [ "python3" ]
CMD [ "manage.py", "runserver", "0.0.0.0:8000" ]