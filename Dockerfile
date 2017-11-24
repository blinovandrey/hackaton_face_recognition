FROM python:3.6
RUN apt-get update -y
RUN apt-get -y install binutils libproj-dev gdal-bin gettext
RUN apt-get -y update RUN apt-get install -y --fix-missing \ build-essential \ cmake \ gfortran \ git \ wget \ curl \ graphicsmagick \ libgraphicsmagick1-dev \ libatlas-dev \ libavcodec-dev \ libavformat-dev \ libboost-all-dev \ libgtk2.0-dev \ libjpeg-dev \ liblapack-dev \ libswscale-dev \ pkg-config \ python3-dev \ python3-numpy \ software-properties-common \ zip \ && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \ mkdir -p dlib && \ git clone -b 'v19.5' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

RUN mkdir -p /var/www

ADD requirements.txt /var/www

RUN pip install pip
RUN pip install uwsgi
RUN pip install --no-cache-dir -r /var/www/requirements.txt

WORKDIR /var/www/absolute

COPY . .
