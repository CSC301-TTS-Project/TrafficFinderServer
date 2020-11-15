from django.contrib.gis.db import models

class TravelTime(models.Model):
    """
        Mock DB table based on travel_time_201809.csv data provided by Raphael.

        Will need to change these fields based on the actual HERE datasets and preform
        the data aggregation queries separately.

        See https://github.com/CityofToronto/bdit_data-sources/tree/master/here
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
