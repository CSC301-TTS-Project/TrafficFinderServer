# Setup

1. Install PostgreSQL 9.6.11 with PostGIS 2.3.7 and pgRouting 2.4.2. Get the database dump from: https://drive.google.com/file/d/1VMj94tSTRI8mglgsfmKW2wdMxEyUBEmw/view?usp=sharing.

2. Install setup venv and install python dependencies: python3 -m pip install -r requirements.txt

3. Install and run local DynamoDB: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html

4. Fill out traffic_finder_server/config/local.ini with relevant fields

5. python3 manage.py runserver


