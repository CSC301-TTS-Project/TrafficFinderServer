from .models import Node, Link, TravelTime

SRID = 4326  # WGS84, GPS Coordinates etc


def shortest_route(start, end):
    """ Get the nodes corresponding the the shortest route between two nodes start and end """

    nodes = Node.objects.raw(
        f"SELECT * FROM nodes NATURAL RIGHT JOIN (SELECT node as node_id from pgr_dijkstra(\'SELECT id, source, target, length as cost FROM links\', {start.node_id}, {end.node_id})) AS path"
    )
    return nodes


def nearest_node(lng, lat):
    """ Get the nearest node, given lng lat coordinates"""
    return Node.objects.raw(f"SELECT * FROM nodes ORDER BY <-> ST_GeometryFromText(\'POINT({lng} {lat})\', {SRID}) LIMIT 1")[0]
