from django.contrib.gis.db import models
from django.db import connection

SRID = 4326  # WGS84, GPS Coordinates etc


class Link(models.Model):
    id = models.BigAutoField(primary_key=True)
    link_dir = models.CharField(max_length=50, blank=True, null=True)
    link_id = models.IntegerField(blank=True, null=True)
    st_name = models.CharField(max_length=50, blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)
    target = models.IntegerField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    wkb_geometry = models.LineStringField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'links'


class NodeManager(models.Manager):
    def nearest_node(self, lng, lat):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM nodes ORDER BY wkb_geometry <-> ST_GeometryFromText(\'POINT(%s %s)\', %s) LIMIT 1",
                [lat, lng, SRID])
            row = cursor.fetchone()
            return self.model(ogc_fid=row[0], node_id=row[1], wkb_geometry=row[2])

    def shortest_route(self, start, end):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM nodes NATURAL RIGHT JOIN (SELECT node AS node_id FROM pgr_dijkstra(\'SELECT id, "
                "source, target, length AS cost FROM links\', %s, %s)) AS path",
                [start.node_id, end.node_id])
            result_list = []
            for row in cursor.fetchall():
                node = self.model(ogc_fid=row[0], node_id=row[1], wkb_geometry=row[2])
                result_list.append(node)
            return result_list


class Node(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    node_id = models.IntegerField(blank=True, null=True)
    wkb_geometry = models.PointField(blank=True, null=True)
    objects = NodeManager()

    class Meta:
        managed = False
        db_table = 'nodes'

    def to_json(self):
        return {'id': self.node_id, 'lat': self.wkb_geometry.y, 'lng': self.wkb_geometry.x }


class TravelTime(models.Model):
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
