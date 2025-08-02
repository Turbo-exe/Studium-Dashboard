# Study Dashboard

![Python](https://img.shields.io/badge/python-3.13.0-blue.svg)
![Django](https://img.shields.io/badge/django-5.2.1-green.svg)
![Project](https://img.shields.io/badge/Portfolio_Project_for-DLBDSOOFPP01__D-blue)
![status](https://img.shields.io/badge/100%25-awesome-green)

## Introduction

This repository holds the project for the IU course DLBDSOOFPP01_D. Created by Felix Asenbauer (IU14110600).
The underlying task for this portfolio project is available on [IU MyCampus](https://mycampus-classic.iu.org/mod/resource/view.php?id=230979).

This readme file covers the following aspects:

- Architecture Overview
- Installation instructions

## Architecture Overview

This project is structured in three main parts:

- **Models** hold the database structure for all data handled in the application.
- **Services** which read data from the database and apply the business logic later used in the dashboard. 
- **Components** are responsible for visualizing the data provided by the Services.

Below you can find architectural UML-class diagrams for these classes:

| Purpose    | Image                             |
|------------|-----------------------------------|
| Models     | ![](documentation\models.png)     |
| Services   | ![](documentation\services.png)   |
| Components | ![](documentation\components.png) |


## Installation

### Docker compose

The easiest option to use run this project is by using docker compose.
To do so, make sure to have Docker (and Compose) installed on your system. To do so, follow these [instructions](https://docs.docker.com/get-started/get-docker/).

Then run the command `docker compose up -d .`.
This will build and start a container running the server for the study dashboard.

### Docker

Instead of using compose, you can also use the Dockerfile and build the image yourself. This again requires docker to be installed on your system.

Firstly, you will need to build the docker image. To do this, run `docker build . -t study-dashboard-iu14110600`

Once this build-process has finished, simply create a container from the previous image. `docker run -d -p 8000:8000 study-dashboard-iu14110600`

Give the server a few seconds to come online. Then you should be able to connect to it using your webbrowser at http://localhost:8000. 


### From source

The last option to have is to manually install all dependencies and start the Django server on your own.
To do this, first make sure you have Python 3.13 installed (download from [here](https://www.python.org/downloads/)).

To begin, create a virtual environment using `python -m venv ./venv` and activate it using `.\venv\Scripts\activate` (windows-only command!).

Next, install all dependencies via `pip install -r requirements.txt`.

Now, create the database `python manage.py migrate --noinput` and tell the program where it is located at by setting 
the environment variable **SQLITE_PATH** to the full path to the database (without the filename). E.g.: `set SQLITE_PATH=C:\Users\<yourUser>\Studium-Dashboard\`.

Lastly, start the server using `python manage.py runserver 8000`.

Once the server has started, you will be able to access the dashboard at http://localhost:8000.

> Note for evaluator: The database will be empty at this point. Check the "Prefilling the database" section below, on how to circumvent this.


## Prefilling the database

For the convenience in evaluating this project, this django repository provides a custom management command `python manage.py prefill_database`.
Once issued, the entire database will be prefilled with database objects for all elements in the frontend. This is not intended for any production setting, but helps to visualize & evaluate this prototype.

> Note: This command is built-in for the Docker-based installation methods.

## Development

### Common Commands

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create language files
python manage.py makemessages -l de

# Compile language files
python manage.py compilemessages    # Note: This requires GNU gettext tools installed

# Prefill database (as described above; requires the database to exist and be fully migrated)
python manage.py prefill_database
```

### Django documentation

For more information on Django, refer to the [official Django documentation](https://docs.djangoproject.com/).

For specific package documentation:
- [Django Components](https://github.com/EmilStenstrom/django-components)
- [Django Tables2](https://django-tables2.readthedocs.io/)
- [Django Filter](https://django-filter.readthedocs.io/)
