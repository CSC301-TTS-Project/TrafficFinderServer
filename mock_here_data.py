"""Script to generate a mock HERE database table based on https://github.com/CityofToronto/bdit_data-sources/tree/master/here"""

import psycopg2
import click
import numpy as np
from datetime import timedelta, datetime
from random import randint
import traceback
import sys


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).total_seconds() // 60) // 5):
        yield start_date + timedelta(minutes=5 * n)


@click.command()
@click.argument('database', type=click.STRING)
@click.argument('username', type=click.STRING)
@click.argument('password', type=click.STRING, default="")
def create_mock_here_data(database, username, password):
    """
    Create mock here data table using travel_time_201809.csv as travel_time table

    Scrapes the link_dir, length, and then randomly populates the other fields

    1 Week of data is approx
    """
    try:
        conn = psycopg2.connect(database=database, user=username, password=password)
    except:
        return click.echo("Unable to connect to database.")

    cur = conn.cursor()
    try:
        cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('here_data',))
        if cur.fetchone()[0]:
            cur.execute("DROP TABLE here_data")
            conn.commit()
        create_table = "CREATE TABLE here_data (link_dir VARCHAR, tx TIMESTAMP, length integer, mean numeric, stddev numeric, confidence integer, pct_85 integer, pct_95 integer, PRIMARY KEY (link_dir, tx))"
        cur.execute(create_table)
        conn.commit()
    except Exception as e:
        return click.echo(e)

    try:
        # populate the table
        cur.execute("SELECT DISTINCT link_dir, length FROM travel_time where random() < 0.01 limit 1000")
        insert_data = []
        row_count = 0
        for row in cur.fetchall():
            for td in daterange(datetime(2018, 9, 1, 0, 0), datetime(2018, 9, 18, 0, 0)):
                date_str = td.strftime("%Y-%m-%d %H:%M:%S")
                recorded_speeds = np.random.randint(30, randint(50, 130), size=randint(5, 15))
                percentiles = [int(p) for p in np.percentile(recorded_speeds, [85, 95], interpolation='nearest')]
                confidence = randint(20, 40)
                mean = np.mean(recorded_speeds)
                std = np.std(recorded_speeds)
                data = (row[0], date_str, row[1], mean, std, confidence, *percentiles)
                insert_data += [data]
            print(f"Done aggregating data for row {row_count}")
            row_count += 1
        records_list_template = ','.join(['%s'] * len(insert_data))
        insert_query = f"INSERT INTO here_data VALUES {records_list_template}"
        cur.execute(insert_query, insert_data)
        conn.commit()
    except Exception as e:
        return click.echo(e)
    conn.close()
    cur.close()


if __name__ == '__main__':
    create_mock_here_data()
