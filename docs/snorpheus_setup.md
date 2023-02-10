## Snorpheus Setup Docs 😴

### Background

The Snorpheus visualization portal is built with [cookiecutter-django](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html), a project template for  production-ready Django projects (best practices built-in!). [Django](https://www.djangoproject.com) is a python-based framework that makes building web applications easier by Django simplifying the code needed to write web authentication (login), API’s, web pages, build and query databases, etc.

Snorpheus runs in a [Docker](https://www.docker.com) container.

Docker summarized on [IBM](https://www.ibm.com/topics/docker) website:

> Docker is an open source platform that enables developers to build, deploy, run, update and manage *containers*—standardized, executable components that combine application source code with the operating system (OS) libraries and dependencies required to **run that code in any environment**.
> 

Basically, Docker makes it easy to set up and run the web application on any computer, without having to worry about operating system conflicts or installing a bunch of new software packages to your own computer.

### Prerequisites

You will first need to install two things to your computer:

- [Git](https://github.com/git-guides/install-git) (to download Snorpheus source code).  Git is a “version control” system for code that tracks changes over time and also makes it easy for multiple people to work on one codebase simultaneously.
- Docker (to run the Snorpheus app in a Docker container). The easiest way to do this is to download [Docker Desktop](https://www.docker.com).

### Database Design

![Database Tables](./database.png?raw=true "Database Tables")

Table Descriptions

- **Patient:** Represents a patient.
- **CollectionPeriod:** Represents one period of time that a patient is assigned to use the Snorpheus system for one or more nights.
- **SleepSession:** Represents one night within a CollectionPeriod.
- **PositionEvent:** Represents one position measurement at a specific timestamp. This table can store (x,y,z) coordinates and rotation angle, in addition to discretized position.
- **AudioFile:** Represents one audio recording from a SleepSession. A SleepSession will have many AudioFiles associated with it, because the night of sleep must be stored in chunks small enough to quickly load in the web browser.
- **AudioLabel:** Represents the YAMNet audio class labels for a specific timestamp.

### Data Requirements

While developing the application, I wrote some helper scripts to import data into the database. They assume the data for one night of sleep is in the following format: 

- The `.wav` file for the full night of sleep (~6-8 hours) is broken into 1 minute chunks with the naming convention: **`session[id]-[chunk-index].wav`** , where **`[id]`**  is replaced with a unique identifier for the session, and **`[chunk_index]`** is replaced with the sequential index of that chunk within the entire audio file, starting with index 000, 001, 002…xxx.  For example, the first minute chunk might be named `session1-000.wav`, the second minute `session1-001.wav`, and the last audio clips might be named `session1-397.wav`
- Each minute chunk has been processed through YAMNet and results of each audio chunk have been written to corresponding `.csv` files with the same naming convention: **`session[id]-[chunk-index].csv`**

> **NOTE:** Your data does not have to be in this exact format—you can modify or write your own scripts to match your data format if you’d like.  However, it is required that **audio clips uploaded to the database be no longer than 1 minute** to ensure it can be quickly loaded into the web browser.
> 

### Setting up Snorpheus on your computer

If you haven’t installed Git and Docker, do this first! 

Then, in Terminal/Command line, `cd` into the directory you’d like to download the project code to.  Then, clone the repository with the following command:

```bash
git clone https://github.com/michellito/snorpheus-django
```

Build Docker image on your computer:

```bash
docker-compose -f local.yml build
```

Apply database migrations (creates database tables in PostgreSQL):

```bash
docker-compose -f local.yml run --rm django python manage.py migrate
```

Create a Django superuser (admin user that has all permissions).  You’ll be prompted for a username, email, and password.

```bash
docker-compose -f local.yml run --rm django python manage.py migrate
```

Now, before we import any data, let’s check if we can run the web app:

```bash
docker-compose local.yml.up
```

Navigate to [localhost:8000](http://localhost:8000) in your web browser, and you should see the site!  Login with the superuser credentials you just created.  

### Import SleepSession data

First we create a test patient.  This script creates a Patient object in the database, as well as a CollectionPeriod containing two SleepSessions, or nights of sleep. This script also randomly generates position data for the night, so you’ll need to write a script to import position data.

```bash
docker-compose -f local.yml run --rm django python manage.py populate_test_patient
```

Then we can populate our audio data for the first SleepSession into the database using the following command:

```bash
docker-compose -f local.yml run --rm django python manage.py populate_audio_files  snorpheus/data/sample_data/audio/session1/ 60 1 1
```

Finally, we can import the audio labels for the audio files

```bash
docker-compose -f local.yml run --rm django python manage.py populate_audio_labels_all  snorpheus/data/sample_data/audio_labels/session2/ 1 1
```