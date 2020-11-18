from django.contrib.gis.db import models
from django.db import connection

SRID = 4326  # WGS84, GPS Coordinates etc, probably migrate to https://epsg.io/2946 down the line, but its fine for now.

class NodeManager(models.Manager):
    def nearest_node(self, lng, lat):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM nodes ORDER BY wkb_geometry <-> ST_GeometryFromText(\'POINT(%s %s)\', %s) LIMIT 1",
                [lat, lng, 4326])
            row = cursor.fetchone()
            return self.model(ogc_fid=row[0], node_id=row[1], wkb_geometry=row[2])


class Node(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    node_id = models.IntegerField(blank=True, null=True)
    wkb_geometry = models.PointField(blank=True, null=True)
    objects = NodeManager()

    class Meta:
        managed = False
        db_table = 'nodes'

    def to_json(self):
        return {'id': self.node_id, 'lat': self.wkb_geometry.y, 'lng': self.wkb_geometry.x}