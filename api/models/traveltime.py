from botocore.compat import total_seconds
from django.db import models
from datetime import datetime
from django.db import connection
from api.models.link import Link
from time import time


class TravelTime(models.Model):
    """
        For visualization purposes only.
    """
    link_dir = models.CharField(primary_key=True, max_length=50)
    tx = models.DateTimeField()
    length = models.FloatField(blank=True, null=True)
    mean = models.FloatField(blank=True, null=True)
    stddev = models.FloatField(blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    pct_50 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'travel_time'
        unique_together = (('link_dir', 'tx'),)

    def to_json(self):
        return {
            'link_dir': self.link_dir,
            'tx': self.tx,
            'length': self.length,
            'mean': self.mean,
            'stddev': self.stddev,
            'confidence': self.confidence,
            'pct_50': self.pct_50
        }

    @staticmethod
    def get_data_for_route_hourly(link_dirs, date_range, days_of_week, hour_range):
        """

        Return hourly aggregated data for the passed links.

        @param link_dirs: A list of link_dirs to include in the aggregation
        @param date_range: String tuple corresponding to the date range e.g. ("2018-09-01", "2018-09-02")
        @param days_of_week: Tuple representing days of week to include in aggregation, e.g. [0, 1, 2] corresponds to sunday, monday, tuesday
        @param hour_range: An hourly range, e.g. [7, 13] for 7AM to 1PM

        @precondition: link_dirs has at least one link.
        """
        start_time = datetime.strptime(
            f'{date_range[0]} {hour_range[0]}:00', '%Y-%m-%d %H:%M').replace(tzinfo=None)
        end_time = datetime.strptime(
            f'{date_range[1]} {hour_range[1]}:00', '%Y-%m-%d %H:%M').replace(tzinfo=None)

        hourly = TravelTime.objects \
            .filter(link_dir__in=link_dirs) \
            .filter(tx__range=[start_time, end_time]) \
            .filter(tx__hour__range=hour_range) \
            .filter(tx__iso_week_day__in=days_of_week) \
            .extra({"hour": "date_trunc('hour', tx)::time"}) \
            .values('hour') \
            .annotate(link_obs=models.Count(1))

        # For whatever reason, the values length values in our DB aren't
        # correct. Recalculate them and related values.
        with connection.cursor() as cursor:
            qs = ','.join('%s' for _ in range(len(link_dirs)))
            cursor.execute(
                f"SELECT SUM(length) "
                f"FROM "
                f"(SELECT DISTINCT links.link_dir, ST_Length(ST_Transform(links.wkb_geometry, 2952)) "
                f"as length FROM links WHERE links.link_dir in ({qs})) as lt",
                link_dirs)

            total_length = cursor.fetchone()[0]
            hourly = hourly.annotate(total_length=models.Value(total_length, models.FloatField())) \
                .annotate(mean_speed=models.Avg('mean')) \
                .annotate(std_dev_speed=models.StdDev('mean')) \
                .annotate(mean_tt=((total_length / 1000) / models.Avg('mean')) * 3600) \
                .annotate(std_dev_tt=((total_length / 1000) / models.StdDev('mean')) * 3600) \
                .annotate(pct_85_speed=models.Aggregate(models.F("mean"),
                                                        function="percentile_cont",
                                                        template="%(function)s(0.85) WITHIN GROUP (ORDER BY %(expressions)s)")) \
                .annotate(pct_95_speed=models.Aggregate(models.F("mean"),
                                                        function="percentile_cont",
                                                        template="%(function)s(0.95) WITHIN GROUP (ORDER BY %(expressions)s)")) \
                .annotate(min_speed=models.Min('mean')) \
                .annotate(max_speed=models.Max('mean'))
            hourly = hourly.annotate(
                full_link_obs=models.Value(
                    ((int((end_time - start_time).seconds) // 60) / 5) *
                    len(link_dirs),
                    models.IntegerField()))

        return hourly

    @staticmethod
    def get_data_for_route(link_dirs, date_range, days_of_week, hour_range):
        """

        Return aggregated data for the passed links.

        @param link_dirs: A list of link_dirs to include in the aggregation
        @param date_range: String tuple corresponding to the date range e.g. ("2018-09-01", "2018-09-02")
        @param days_of_week: Tuple representing days of week to include in aggregation, e.g. [0, 1, 2] corresponds to sunday, monday, tuesday
        @param hour_range: An hourly range, e.g. [7, 13] for 7AM to 1PM

        @precondition: link_dirs has at least one link.
        """
        start_time = datetime.strptime(
            f'{date_range[0]} {hour_range[0]}:00', '%Y-%m-%d %H:%M').replace(tzinfo=None)
        end_time = datetime.strptime(
            f'{date_range[1]} {hour_range[1]}:00', '%Y-%m-%d %H:%M').replace(tzinfo=None)

        start = time()
        hourly = TravelTime.objects \
            .filter(link_dir__in=link_dirs) \
            .filter(tx__range=[start_time, end_time]) \
            .filter(tx__hour__range=hour_range) \
            .filter(tx__iso_week_day__in=days_of_week) \
            .values('link_dir') \
            .annotate(link_obs=models.Count(1))
        end = time()
        print("Hourly Model 117: ", end-start)

        # For whatever reason, the values length values in our DB aren't
        # correct. Recalculate them and related values.
        # with connection.cursor() as cursor:
        #     qs = ','.join('%s' for _ in range(len(link_dirs)))
        #     cursor.execute(
        #         f"SELECT DISTINCT travel_time.link_dir, length "
        #         f"FROM travel_time WHERE travel_time.link_dir in ({qs})",
        #         link_dirs)
        #     lengths = cursor.fetchall()

        #     total_length = 0
        #     for l in lengths:
        #         total_length += l[1]

        # For whatever reason, the values length values in our DB aren't
        # correct. Recalculate them and related values.
        with connection.cursor() as cursor:

            start = time()
            qs = ','.join('%s' for _ in range(len(link_dirs)))
            cursor.execute(f"SELECT length, link_dir "
                           f"FROM "
                           f"(SELECT DISTINCT links.link_dir as link_dir, ST_Length(ST_Transform(links.wkb_geometry, 2952)) "
                           f"as length FROM links WHERE links.link_dir in ({qs})) as lt",
                           link_dirs)
            end = time()
            print("SQL Query 146: ", end - start)

            start = time()
            total_length = 0

            cursor_query = {link_dir: float(length) for
                            length, link_dir in cursor.fetchall()}
            total_length = sum(cursor_query.values())
            print(cursor_query)

            hourly = hourly.annotate(mean=models.Avg("mean")/1000)\
                        .annotate(std_dev_tt=((total_length / 1000) / models.StdDev('mean')) * 3600) \
                        .annotate(pct_85_speed=models.Aggregate(models.F("mean"),
                                                        function="percentile_cont",
                                                        template="%(function)s(0.85) WITHIN GROUP (ORDER BY %(expressions)s)")) \
                        .annotate(pct_95_speed=models.Aggregate(models.F("mean"),
                                                        function="percentile_cont",
                                                        template="%(function)s(0.95) WITHIN GROUP (ORDER BY %(expressions)s)"))  \
                        .annotate(min_speed=models.Min('mean')) \
                        .annotate(max_speed=models.Max('mean'))

            travel_times, standard_deviations, perc_85, perc_95, min_speeds, max_speeds = [], [], [], [], [], [] 

            for entry in hourly.all():
                if entry['link_dir'] in cursor_query:
                    travel_times = cursor_query[entry['link_dir']] / entry['mean']

            length = len(travel_times)
            tt_mean = sum(travel_times) / \
                length * 3600
            harmonic_mean = sum(cursor_query.values()) / total_length
            harmonic_std = sum(standard_deviations) / length
            harmonic_perc_85 = sum(perc_85)/length
            harmonic_perc_05 = sum(perc_95)/length
            harmonic_min = sum(min_speeds)/length
            harmonic_max = sum(max_speeds)/length

            end = time()
            print("Total Length = ", total_length)
            print("Summing over length 155: ", end-start)

            start = time()
            hourly = hourly.annotate(std_dev_speed=models.StdDev('mean')) \
                .annotate(std_dev_tt=((total_length / 1000) / models.StdDev('mean')) * 3600) \
                .annotate(pct_85_speed=models.Aggregate(models.F("mean"),
                                                        function="percentile_cont",
                                                        template="%(function)s(0.85) WITHIN GROUP (ORDER BY %(expressions)s)")) \
                .annotate(pct_95_speed=models.Aggregate(models.F("mean"),
                                                        function="percentile_cont",
                                                        template="%(function)s(0.95) WITHIN GROUP (ORDER BY %(expressions)s)")) \
                .annotate(min_speed=models.Min('mean')) \
                .annotate(max_speed=models.Max('mean'))
            end = time()
            print("hourly 162: ", end-start)

            start = time()
            hourly = list(hourly.annotate(
                full_link_obs=models.Value(
                    ((int((end_time - start_time).seconds) // 60) / 5) *
                    len(link_dirs),
                    models.IntegerField())).all())
            end = time()
            print("Hourly 179: ", end-start)

        return hourly
