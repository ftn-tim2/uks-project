FROM django:1.8-python3
RUN apt-get update
RUN easy_install pip
RUN pip install uwsgi
RUN pip install mysqlclient
ADD . /opt/apps/djdocker
RUN apt-get install libjpeg62-turbo-dev -y
RUN apt-get install zlib1g-dev -y
RUN apt-get install python-dev -y
RUN ln -s -T /usr/include/freetype2/ /usr/include/freetype
RUN pip install -r /opt/apps/djdocker/requirements.txt
CMD ["python", "/opt/apps/djdocker/manage.py","runserver", "0.0.0.0:8000"]
