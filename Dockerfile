FROM python:3.6
RUN apt-get update -y
RUN apt-get -y install binutils libproj-dev gdal-bin gettext

RUN mkdir -p /var/www

ADD requirements.txt /var/www

RUN pip install pip
RUN pip install uwsgi
RUN pip install --no-cache-dir -r /var/www/requirements.txt

WORKDIR /var/www/absolute

COPY . .
