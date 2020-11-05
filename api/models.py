# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class Links(models.Model):
    id = models.BigAutoField(primary_key=True)
    link_dir = models.CharField(max_length=-1, blank=True, null=True)
    link_id = models.IntegerField(blank=True, null=True)
    st_name = models.CharField(max_length=-1, blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)
    target = models.IntegerField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    wkb_geometry = models.LineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'links'


class Nodes(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    node_id = models.IntegerField(blank=True, null=True)
    wkb_geometry = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nodes'


class TravelTime(models.Model):
    link_dir = models.CharField(primary_key=True, max_length=-1)
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
