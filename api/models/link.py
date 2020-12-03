from django.contrib.gis.db import models
from django.db import connection


class LinkManager(models.Manager):

    def shortest_route_links(self, start, end):
        """
        Return the list corresponding to the shortest route (with Dijkstra) using PSQL query. 
        """
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, link_dir, link_id, st_name, source, target, wkb_geometry "
                "FROM links INNER JOIN (SELECT * FROM pgr_dijkstra(\'SELECT id, "
                "source, target, length AS cost FROM links\', %s, %s)) AS path ON edge=id ORDER BY path_seq",
                [start.node_id, end.node_id])
            result_list = []
            for row in cursor.fetchall():
                columns = [col[0] for col in cursor.description]
                result_list.append(self.model(**dict(zip(columns, row))))
            return result_list


class Link(models.Model):
    id = models.BigAutoField(primary_key=True)
    link_dir = models.CharField(max_length=50, blank=True, null=True)
    link_id = models.IntegerField(blank=True, null=True)
    st_name = models.CharField(max_length=50, blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)
    target = models.IntegerField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    wkb_geometry = models.LineStringField(blank=True, null=True)
    objects = LinkManager()

    class Meta:
        managed = False
        db_table = 'links'
