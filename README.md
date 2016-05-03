# uks-project

notes: docker-entrypoint.sh will try to migrate to the database every time the web app is started.
If the MySQL database was emtpy it will fail when it comes to createing some unnamed tables. - no idea why
Since it fails on a certain point, we need to restart the application, now it will create the remaining tables.

After we have all the tables created we need to run manage.py createsuperuser.
