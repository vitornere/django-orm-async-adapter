FROM python:3.9

RUN mkdir /code
WORKDIR /code

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE settings

ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/

RUN chmod +x ./start.sh
ENTRYPOINT ["./start.sh"]
