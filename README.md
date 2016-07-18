# uks-project

## Short description

This project is mainly focusing around creating issue tracking system for an existing Git repository.
The web page is usable only with a registered account. This account has possibility to contribute to any project.
All users may create a new issue for a project. Users may also comment on the issues as well. Once a project is created the owner of the project may redifine a few properties. The owner may add new statuses of the issues, delete or edit the existing ones. The owner also able to change the issue types, milestones and priorities. Issues and commits can be linked together.

Other project that were used during the development of this application:

1. [Simple MySQL image](https://hub.docker.com/r/tim2/mysqldb/)
2. [Forked Shipyard image](https://hub.docker.com/r/tim2/shipyard/) 
3. [Forked Shipyard Repository](https://github.com/ftn-tim2/shipyar)
4. [Link to Shipyard master Repository](https://github.com/shipyard/shipyard)
5. [Link to the django generator](https://github.com/ftn-tim2/jsd-project)

## DockerHub integration

[Link to dockerhub image](https://hub.docker.com/r/tim2/uks-project/)
or use 
**docker pull tim2/uks-project**

To build your own image please use the DockerFile on the [root](Dockerfile).

## Continous delivery setup

The following diagram shows the setup that was used to automate the deployment on the FTN server.
After a commit on the master we have the latest code deployed on the accptance server in 10 minutes.

![alt tag](https://github.com/ftn-tim2/uks-project/blob/master/FTN%20continous%20delivery.PNG)

## Team members with the division of work

* [Berkó Szabolcs](https://github.com/szberko)
  * setting up Docker image
  * implement WebHook in Shipyard project
  * setup continous delivery
  * generate basic Django application
  * define model
  * UI implementations
  * UI bugfixes
  * setup Coded UI tests
* [Filip Frank](https://github.com/Pazzo92)
  * develop Django generator
  * define model
  * generate basic Django application
  * UI implementations
  * UI bugfixes
  * connecting application with project's github repository
  * model changes
* [Ana Lukić](https://github.com/ra28)
  * UI implementations
  * UI bugfixes
  * model changes
  * UI testing
* [Kovács József](https://github.com/thekrushka)
  * develop Django generator
  * setting up Docker image
  * implement WebHook in Shipyard project
  * setup continous delivery
  * UI bugfixes
  * model changes

notes: docker-entrypoint.sh will try to migrate to the database every time the web app is started.
If the MySQL database was emtpy it will fail when it comes to createing some unnamed tables. - no idea why
Since it fails on a certain point, we need to restart the application, now it will create the remaining tables.
