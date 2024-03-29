## Snorpheus Setup Docs 😴

### Background

The Snorpheus visualization portal is built with [cookiecutter-django](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html), a project template for  production-ready Django projects. [Django](https://www.djangoproject.com) is a python-based framework that makes building web applications easier by Django simplifying the code needed to build the components commonly needed for web apps, such as authentication (login), web APIs, and databases.

Snorpheus runs in a [Docker](https://www.docker.com) container.

Docker summarized on [IBM](https://www.ibm.com/topics/docker) website:

> Docker is an open source platform that enables developers to build, deploy, run, update and manage *containers*—standardized, executable components that combine application source code with the operating system (OS) libraries and dependencies required to **run that code in any environment**.
> 

Docker makes it easy to set up and run the web application on any computer, without having to worry about operating system conflicts or installing a bunch of new software packages to your own computer.

### Prerequisites

You will first need to install two things to your computer:

- [Git](https://github.com/git-guides/install-git) (to download Snorpheus source code).  Git is a “version control” system for code that tracks changes over time and also makes it easy for multiple people to work on one codebase simultaneously.
- Docker (to run the Snorpheus app in a Docker container). The easiest way to do this is to download [Docker Desktop](https://www.docker.com).

### Database Design

The database contains the following tables for storing the patient’s sleep data. Below the tables and fields are described.

**Patient:** Represents a patient. 

- `id` : Autogenerated ID (you do not need to provide this, as it will be added automatically)
- `first_name` : Patient’s first name
- `last_name` : Patient’s last name

**CollectionPeriod:** Represents one period of time that a patient is assigned to use the Snorpheus system for one or more nights.

- `id` : Autogenerated ID (you do not need to provide this, as it will be added automatically)
- `patient` : `id` of the **Patient** object for which this **CollectionPeriod** is for
- `start_date` : start date for data collection in format `yyyy-mm-dd`
- `end_date` : end date for data collection in format `yyyy-mm-dd`

For example, if the patient was assigned to wear the device the night of Feb 14, 2023, the start date would be `2023-02-14`, and the end date would be `2023-02-15`

**SleepSession:** Represents one night within a CollectionPeriod.

- `id` : Autogenerated ID (you do not need to provide this, as it will be added automatically)
- `collection_period` : `id` of the **CollectionPeriod** for which this **SleepSession** is part of
- `device_start_time` : start time of data collection, according to the device clock. This should be a python `datetime` object.
- `device_end_time` : end time of data collection, according to the device clock. This should be a python `datetime` object.
- `true_start_time` : in the case that the device clock is inaccurate, this field allows the true start time to be manually entered.

**PositionEvent:** Represents one position measurement at a specific timestamp. This table stores rotation angle, in addition to discretized position.

- `id` : Autogenerated ID (you do not need to provide this, as it will be added automatically)
- `sleep_session` : `id` of **SleepSession**
- `angle` : Rotation angle of device.
- `position`: Discretized position, choices are **Left**, **Right**, **Prone**, **Supine**, and **Other**.  “Other” would be used in the case the patient is not lying down at any point (sitting or standing up)
- `seconds_elapsed`: timestamp of this **PositionEvent** in the form of seconds elapsed since start of data collection (seconds since SleepSession `device_start_time`)
- `timestamp`: legacy field, this can be ignored

NOTE: While the device can measure position hundreds of times per second, it would be sufficient to capture position once per second.

**AudioFile:** Represents one audio recording from a SleepSession. A SleepSession will have many AudioFiles associated with it, because the night of sleep must be stored in chunks small enough to quickly load in the web browser.

- `id` : Autogenerated ID (you do not need to provide this, as it will be added automatically)
- `sleep_session` : `id` of **SleepSession**
- `audio_file` : <1 minute audio file chunk in `.wav` format.  This will be a Django File object.
- `seconds_elapsed` : start time of this audio file, in the form of seconds elapsed since start of data collection (seconds since SleepSession `device_start_time`)
- `start_time`: legacy field, this can be ignored

**AudioLabel:** Represents the YAMNet audio class labels for a specific timestamp.

- `id` : Autogenerated ID (you do not need to provide this, as it will be added automatically)
- `audio_file` : `id` of **AudioFile** for this **AudioLabel**
- `seconds_elapsed` : timestamp of this **AudioLabel**, in the form of seconds elapsed since start of data collection (seconds since SleepSession `device_start_time`)
- `label_1` : highest scoring YAMNET label for this timestamp
- `label_2` : second highest scoring YAMNET label
- `label_3` : third highest scoring YAMNET label
- `score_1` : YAMNet score for label_1
- `score_2` : YAMNet score for label_2
- `score_3` : YAMNet score for label_3

The diagram below illustrates the relations between the database tables.

![Database Tables](./images/database.png?raw=true "Database Tables")

### Data Requirements

While developing the application, I wrote some helper scripts to import data into the database. They assume the data for one night of sleep is in the following format: 

- The `.wav` file for the full night of sleep (~6-8 hours) is broken into 1 minute chunks with the naming convention: `**session[id]-[chunk-index].wav**` , where **`[id]`**  is replaced with a unique identifier for the session, and `**[chunk_index]**` is replaced with the sequential index of that chunk within the entire audio file, starting with index 000, 001, 002…xxx.  For example, the first minute chunk might be named `session1-000.wav`, the second minute `session1-001.wav`, and the last audio clips might be named `session1-397.wav`
- Each minute chunk has been processed through YAMNet and results of each audio chunk have been written to corresponding `.csv` files with the same naming convention: **`session[id]-[chunk-index].csv`**
- All audio files for a single SleepSession are placed in `snorpheus/data/sample_data/audio/session[id]`
- All audio label CSV files for the audio files are placed in `snorpheus/data/sample_data/audio_labels/session[id]`

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

Create a Django superuser (admin user that has all permissions).  You’ll be prompted for a username, email, and password.  Save this info somewhere, as you’ll need it to login to the web app.

```bash
docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

Now, before we import any data, let’s check if we can run the web app:

```bash
docker-compose -f local.yml up
```

Navigate to [localhost:8000](http://localhost:8000) in your web browser, and you should see the site! Login with the superuser credentials you just created.

The first time you login, you'll be asked to verify your email address by clicking an emailed confirmation link. Since we're running locally on our machine, the email does not actually get sent, but instead will be printed to the console/terminal where the `docker-compose -f local.yml up` command is running. You should see something like below, and you can copy the confirmation link and paste it into your browser to confirm your email.

![Email Confirmation](./images/confirm_email.png?raw=true "Email Confirmation")

The visualization portal is located at localhost:8000 and the Admin section where you can add Patients and CollectionPeriods is located at localhost:8000/admin.

### Import SleepSession data

NOTE: These scripts were created for my own use for creating test patients and data, these will likely need to be modified.  The scripts can be found in `snorpheus/data/managment/commands`

1. **populate_test_patient.py**

This script creates a Patient object in the database, as well as a CollectionPeriod containing two SleepSessions, or nights of sleep. This script also randomly generates position data for the night, so you’ll need to write a script to import position data collected with the device.

```bash
docker-compose -f local.yml run --rm django python manage.py populate_test_patient
```

2. **populate_audio_files.py**

This command creates AudioFile objects for all audio files located in the specified directory and links them to the specified **Patient** and **SleepSession**. The arguments for this command are as follows:

- directory: directory to load audio files from
- audio_chunk_length: the length of each audio chunk in seconds
- patient_id: ID of the patient
- session_id: ID of the SleepSession for which these audio files are for

The command can be run like this:

```bash
docker-compose -f local.yml run --rm django python manage.py populate_audio_files <directory> <audio_chunk_length> <patient_id> <session_id>
```

An example for loading all audio files located in directory `snorpheus/data/sample_data/audio/session1/`  to one of the SleepSessions created in step 1 would be:

```bash
docker-compose -f local.yml run --rm django python manage.py populate_audio_files  snorpheus/data/sample_data/audio/session1/ 60 1 1
```

- We use 60 for `audio_chunk_length` because each audio chunk is 1 minute
- We use `patient_id` of 1, since the test patient created in step 1 has an ID of 1, since they are the first patient in the database.
- We use `session_id` of 1, since we want to load the audio files to the first night of sleep for this patient, which happens to be the first SleepSession in the database.

3. **populate_audio_labels_all.py**

Finally, we can import the audio labels for the audio files.  This script creates AudioLabel objects for the YAMNet labels that are currently in CSV format.  This command operates similarly to **populate_audio_files.py** where the arguments are:

- The directory containing the CSV files to load
- Patient ID
- SleepSession ID to load YAMNet labels to

```bash
docker-compose -f local.yml run --rm django python manage.py populate_audio_labels_all  snorpheus/data/sample_data/audio_labels/session1/ 1 1
```

### Visualize the Data

After importing the position and audio data, we can now run the web app again to visualize it:

```bash
docker-compose local.yml up
```

Navigate to [localhost:8000](http://localhost:8000) in your web browser, and login with the superuser credentials. The visualization portal is located at localhost:8000

Here you can use the sidebar to search patient ID, and select SleepSessions to visualize.

![Visualization Portal](./images/snorpheus_portal.png?raw=true "Visualization Portal")





