from django.db import models
from datetime import datetime
from .link import Link


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

        link_hourly = TravelTime.objects \
            .filter(link_dir__in=link_dirs) \
            .filter(tx__range=[start_time, end_time]) \
            .filter(tx__hour__range=hour_range) \
            .filter(tx__iso_week_day__in=days_of_week) \
            .extra({"hour": "date_trunc('hour', tx)::time"}) \
            .values('link_dir', 'hour', 'length').annotate(hourly_mean_tt=models.Avg('mean'),
                                                           link_obs=models.Count(1),
                                                           pct_85=models.Aggregate(
                                                               models.F("mean"),
                                                               function="percentile_cont",
                                                               template="%(function)s(0.85) WITHIN GROUP (ORDER BY %(expressions)s)",
                                                           ),
                                                           pct_95=models.Aggregate(
                                                               models.F("mean"),
                                                               function="percentile_cont",
                                                               template="%(function)s(0.95) WITHIN GROUP (ORDER BY %(expressions)s)",
                                                           ))

        return link_hourly
