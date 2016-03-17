FROM django:1.8-python3
RUN apt-get update
RUN easy_install pip
RUN pip install uwsgi
RUN pip install mysqlclient
ADD . /opt/apps/djdocker
RUN apt-get install libjpeg62-turbo-dev -y
RUN apt-get install zlib1g-dev -y
RUN apt-get install python-dev -y
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:git-core/ppa -y
RUN apt-get update
RUN apt-get install git -y
RUN ln -s -T /usr/include/freetype2/ /usr/include/freetype
RUN pip install -r /opt/apps/djdocker/requirements.txt
CMD ["python", "/opt/apps/djdocker/manage.py","runserver", "0.0.0.0:8000"]
