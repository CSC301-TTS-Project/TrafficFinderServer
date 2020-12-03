# Local Setup

1. Install PostgreSQL 9.6.11 with PostGIS 2.3.7 and pgRouting 2.4.2. Get the database dump from: https: // drive.google.com / file / d / 1VMj94tSTRI8mglgsfmKW2wdMxEyUBEmw / view?usp = sharing
* Note: supposedly this step has issues with certain dependencies not fully working on windows

2. Setup venv and install python dependencies: `python3 - m pip install - r requirements.txt`

3. Install AWS cli and run aws configure

3. Install and run local DynamoDB: https://docs.aws.amazon.com / amazondynamodb / latest / developerguide / DynamoDBLocal.DownloadingAndRunning.html

4. Fill out traffic_finder_server / config / local.ini with relevant fields for your setup(database, database users, and table names etc.)

5. Do django migrations: `python3 manage.py makemigrations & & python3 manage.py migrate`

6. Run tests: `python manage.py test --keepdb --nologcapture`

7. Run backend: `python manage.py runserver`
