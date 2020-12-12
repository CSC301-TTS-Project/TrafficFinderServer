import itertools

from api.models.link import Link
from api.models.node import Node


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
        self.start_node = Node.objects.get(
            node_id=links[0].source) if start is None else start
        self.end_node = Node.objects.get(
            node_id=links[-1].target) if end is None else start

        self.link_dirs = [link.link_dir for link in links]
        # [{'lat': <val>, 'lng': <val>}, ...]
        lng_lat_tuples = list(itertools.chain.from_iterable(
            link.wkb_geometry.tuple for link in links))
        seen_tuples = set()
        self.coordinates = []
        for tup in lng_lat_tuples:
            if tup not in seen_tuples:
                self.coordinates.append(tup)
            seen_tuples.add(tup)

    def to_json(self):
        return {
            'start_node': self.start_node.to_json(),
            'end_node': self.end_node.to_json(),
            'coordinates': self.coordinates,
            'link_dirs': self.link_dirs
        }

    def to_geojson_feature(self):
        return {
            "type": "LineString",
            "metadata": {
                "start_node": self.start_node.to_json(),
                'end_node': self.end_node.to_json(),
                "link_dirs": self.link_dirs
            },
            "coordinates": self.coordinates
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
