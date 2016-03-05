FROM django:1.8-python3
RUN apt-get update
RUN easy_install pip
RUN pip install uwsgi
RUN pip install mysqlclient
ADD . /opt/apps/djdocker
RUN pip install -r /opt/apps/djdocker/requirements.txt
RUN (cd /opt/apps/djdocker && python manage.py migrate --noinput)
RUN (cd /opt/apps/djdocker && python manage.py collectstatic --noinput)
EXPOSE 8000
CMD ["python", "/opt/apps/djdocker/manage.py","runserver", "0.0.0.0:8000"]