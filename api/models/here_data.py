from django.contrib.gis.db import models
from django.db import connection
from datetime import datetime


class HereData(models.Model):
    link_dir = models.CharField(primary_key=True, max_length=50)
    tx = models.DateTimeField()
    length = models.IntegerField(blank=True, null=True)
    mean = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    stddev = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    confidence = models.IntegerField(blank=True, null=True)
    pct_85 = models.IntegerField(blank=True, null=True)
    pct_95 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'here_data'
        unique_together = (('link_dir', 'tx'),)

    def to_json(self):
        return {
            'link_dir': self.link_dir,
            'tx': self.tx,
            'length': self.length,
            'mean': self.mean,
            'stddev': self.stddev,
            'confidence': self.confidence,
            'pct_85': self.pct_85,
            'pct_95': self.pct_95
        }

    @staticmethod
    def get_data_for_route(link_dirs, date_range, days_of_week, hour_range):
        """
        @param link_dirs: A list of link_dirs to include in the aggregation
        @param date_range: String tuple corresponding to the date range e.g. ("2018-09-01", "2018-09-02")
        @param days_of_week: Tuple representing days of week to include in aggregation, e.g. [0, 1, 2] corresponds to sunday, monday, tuesday
        @param hour_range: An hourly range, e.g. ["07:00", "13:00"]
        """

        start_time = datetime.strptime(f'{date_range[0]} {hour_range[0]}', '%Y-%m-%d %I:%M')
        end_time = datetime.strptime(f'{date_range[1]} {hour_range[1]}', '%Y-%m-%d %I:%M')

        agg = HereData.objects.filter(link_dir__in=link_dirs) \
            .filter(tx__range=[start_time, end_time]) \
            .filter(tx__iso_week_day__in=days_of_week).extra(
            select={
                'hour': "date_part(\'hour\', \"tx\")"
            }
        )

        print({**agg[0].to_json(), 'hour': agg[0].hour})
