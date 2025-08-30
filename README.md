# Study Dashboard

![Python](https://img.shields.io/badge/python-3.13.3-blue.svg)
![Django](https://img.shields.io/badge/django-5.2.3-green.svg)
![Project](https://img.shields.io/badge/Portfolio_Project_for-DLBDSOOFPP01__D-blue)
![status](https://img.shields.io/badge/100%25-awesome-green)

## Introduction

This repository holds the project for the IU course DLBDSOOFPP01_D. Created by Felix Asenbauer (IU14110600).
The underlying task for this portfolio project is available
on [IU MyCampus](https://mycampus-classic.iu.org/mod/resource/view.php?id=230979).

This readme file covers the following aspects:

- Architecture Overview
- Installation instructions
- Tips & Tricks for Development

## Architecture Overview

This project is structured in three main parts:

- **Models** hold the database structure for all data handled in the application.
- **Services** which read data from the database and apply the business logic later used in the dashboard.
- **Components** are responsible for visualizing the data provided by the Services.

If you want to deep dive into the technical details for this project, check out these files for more details:

- [documentation/responsibilities.md](./documentation/responsibilities.md) - **The what** - This file goes into details what packages
  and classes there are and what functionality they provide. Here you will also find the UML diagrams for all classes.
- [documentation/decisions.md](./documentation/decisions.md) - **The why** - Here I lay out why the project was written in the way it was. Why create certain classes, why write code in a specific way - and so on.  

## Installation

### (easiest) - Docker compose

The easiest option to use run this project is by using docker compose.
To do so, make sure to have Docker (and Compose) installed on your system. To do so, follow
these [instructions](https://docs.docker.com/get-started/get-docker/).

Then run the command `docker compose up -d`.
This will build and start a container running the server for the study dashboard.

### (easy) - Docker

Instead of using compose, you can also use the Dockerfile and build the image yourself. This again requires docker to be
installed on your system.

Firstly, you will need to build the docker image. To do this, run `docker build . -t study-dashboard-iu14110600`

Once this build-process has finished, simply create a container from the previous image.
`docker run -d -p 8000:8000 study-dashboard-iu14110600`

Give the server a few seconds to come online. Then you should be able to connect to it using your webbrowser
at http://localhost:8000.

### (advanced) - From source

The most advanced option is to manually install all dependencies and start the Django server on your own.
To do this, first make sure you have Python 3.13.3 installed (download from [here](https://www.python.org/downloads/)).

To begin, create a virtual environment using `python -m venv ./venv` and activate it using `.\venv\Scripts\activate` (
windows-only command!).

Next, install all dependencies via `pip install -r requirements.txt`.

Now, create the database `python manage.py migrate --noinput` and tell the program where it is located at by setting
the environment variable **SQLITE_PATH** to the full path to the database (without the filename):

- (Windows Command Prompt) `set SQLITE_PATH=C:\Users\<yourUser>\Studium-Dashboard\`
- (Windows Powershell) `$env:SQLITE_PATH = "C:\Users\<yourUser>\Studium-Dashboard\"`

Lastly, start the server using `python manage.py runserver 8000`.

Once the server has started, you will be able to access the dashboard at http://localhost:8000.

> Note for evaluator: The database will be empty at this point. Check the "Prefilling the database" section below, on
> how to circumvent this.

## Prefilling the database

For the convenience in evaluating this project, this django repository provides a custom management command
`python manage.py prefill_database`.
Once issued, the entire database will be prefilled with database objects for all elements in the frontend. This is not
intended for any production setting, but helps to visualize & evaluate this prototype.

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

### Management Commands

Some objects cannot be added, updated or delete through the frontend, as this was not scope of this prototype.
To still provide this data-manipulation capability, the management commands below can be used.

#### Create Commands

| Command           | Description            | Example                                                                                                           |
|-------------------|------------------------|-------------------------------------------------------------------------------------------------------------------|
| `create_degree`   | Creates a new degree   | `python manage.py create_degree "Computer Science" "BSC" --description "Bachelor of Science in Computer Science"` |
| `create_semester` | Creates a new semester | `python manage.py create_semester "Winter 2024/2025" 1 2024 "2024-10-01" "2025-03-31"`                            |
| `create_course`   | Creates a new course   | `python manage.py create_course "Programming Basics" "PROG101" 1 --ects 5`                                        |
| `create_exam`     | Creates a new exam     | `python manage.py create_exam "Final Exam" 1 "WE"`                                                                |
| `create_student`  | Creates a new student  | `python manage.py create_student "John Doe" "John" "Doe" "john.doe@example.com" 1 1`                              |

#### Update Commands

| Command           | Description                  | Example                                                                      |
|-------------------|------------------------------|------------------------------------------------------------------------------|
| `update_degree`   | Updates an existing degree   | `python manage.py update_degree 1 --name "Data Science" --degree_type "MSC"` |
| `update_semester` | Updates an existing semester | `python manage.py update_semester 1 --name "Summer 2025" --year 2025`        |
| `update_course`   | Updates an existing course   | `python manage.py update_course 1 --name "Advanced Programming" --ects 6`    |
| `update_exam`     | Updates an existing exam     | `python manage.py update_exam 1 --exam_type "PO"`                            |
| `update_student`  | Updates an existing student  | `python manage.py update_student 1 --email "new.email@example.com"`          |

#### Delete Commands

| Command           | Description        | Example                              |
|-------------------|--------------------|--------------------------------------|
| `delete_degree`   | Deletes a degree   | `python manage.py delete_degree 1`   |
| `delete_semester` | Deletes a semester | `python manage.py delete_semester 1` |
| `delete_course`   | Deletes a course   | `python manage.py delete_course 1`   |
| `delete_exam`     | Deletes an exam    | `python manage.py delete_exam 1 `    |
| `delete_student`  | Deletes a student  | `python manage.py delete_student 1`  |

All delete commands prompt for confirmation unless the `--force` flag is used. They also warn about associated objects
that will be deleted.

### Django documentation

For more information on Django, refer to the [official Django documentation](https://docs.djangoproject.com/).

For specific package documentation:

- [Django Components](https://github.com/EmilStenstrom/django-components)
- [Django Tables2](https://django-tables2.readthedocs.io/)
- [Django Filter](https://django-filter.readthedocs.io/)
