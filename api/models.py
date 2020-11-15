import itertools

from django.contrib.gis.db import models
from django.db import connection

SRID = 4326  # WGS84, GPS Coordinates etc


class LinkManager(models.Manager):

    def shortest_route_links(self, start, end):
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


class NodeManager(models.Manager):
    def nearest_node(self, lng, lat):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM nodes ORDER BY wkb_geometry <-> ST_GeometryFromText(\'POINT(%s %s)\', %s) LIMIT 1",
                [lat, lng, SRID])
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


class Segment:
    """
    A Segment consists of an unpacked sequence of links that correspond to a parts of a path.

    @attributes:
        start_node: the node corresponding to the start of this segment
        end_node: the node corresponding to the end of this segment
        link_dirs: ids used to index into traffic data
        coordinates: coordinates that define a the line for this segment. Is an empty list for singular segments.
    """

    def __init__(self, links, start=None, end=None):
        """
        @param links: A list of links that define this segment

        If the segment consists of only one node,
        """
        self.start_node = Node.objects.get(node_id=links[0].source) if start is None else start
        self.end_node = Node.objects.get(node_id=links[-1].target) if end is None else start

        self.link_dirs = [link.link_dir for link in links]
        # [{'lat': <val>, 'lng': <val>}, ...]
        self.coordinates = [dict(zip(["lat", "lng"], tup)) for tup in
                            list(itertools.chain.from_iterable(link.wkb_geometry.array for link in links))]

    def to_json(self):
        return {
            'start_node': self.start_node.to_json(),
            'end_node': self.end_node.to_json(),
            'coordinates': self.coordinates
        }

    @staticmethod
    def route_segment_between_nodes(start, end):
        """
        Create segment that represents the shortest path between two nodes.

        @param start: Starting Node
        @param end: Ending Node
        @return: segment that represents the shortest path between two nodes.
        """
        return Segment(Link.objects.shortest_route_links(start, end))

    @staticmethod
    def singular(node):
        """
        Create a singular segment.

        A singular segment consists of only one node, and no links.
        @param node: the singular node in this segment
        @return: a singular segment
        """
        return Segment([], start=node, end=node)


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
