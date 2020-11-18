from django.db import models
from datetime import datetime
from django.db import connection
from .node import SRID


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
    def get_data_for_route(link_dirs, date_range, days_of_week, hour_range):
        """
        #TODO: min/max speed, street names

        Return hourly aggregated data for the passed links.

        @param link_dirs: A list of link_dirs to include in the aggregation
        @param date_range: String tuple corresponding to the date range e.g. ("2018-09-01", "2018-09-02")
        @param days_of_week: Tuple representing days of week to include in aggregation, e.g. [0, 1, 2] corresponds to sunday, monday, tuesday
        @param hour_range: An hourly range, e.g. [7, 13] for 7AM to 1PM
        """

        start_time = datetime.strptime(f'{date_range[0]} {hour_range[0]}:00', '%Y-%m-%d %H:%M').replace(tzinfo=None)
        end_time = datetime.strptime(f'{date_range[1]} {hour_range[1]}:00', '%Y-%m-%d %H:%M').replace(tzinfo=None)

        hourly = TravelTime.objects \
            .filter(link_dir__in=link_dirs) \
            .filter(tx__range=[start_time, end_time]) \
            .filter(tx__hour__range=hour_range) \
            .filter(tx__iso_week_day__in=days_of_week) \
            .extra({"hour": "date_trunc('hour', tx)::time"}) \
            .values('hour') \
            .annotate(link_obs=models.Count(1))

        # For whatever reason, the values length values in our DB aren't correct. Recalculate them and related values.
        with connection.cursor() as cursor:
            qs = ','.join('%s' for _ in range(len(link_dirs)))
            cursor.execute(
                f"SELECT SUM(length) "
                f"FROM "
                f"(SELECT DISTINCT links.link_dir, ST_Length(ST_Transform(links.wkb_geometry, {SRID})) "
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
                                                        template="%(function)s(0.95) WITHIN GROUP (ORDER BY %(expressions)s)"))
            hourly = hourly.annotate(
                full_link_obs=models.Value(((int((end_time - start_time).seconds) // 60) / 5) * len(link_dirs),
                                           models.IntegerField()))

        return hourly
