import os
from neo4j import GraphDatabase
import googlemaps

googleKey = os.environ.get('GOOGLEAPI')
class Neo4jGoogleMap:

    def __init__(self, googleKey, neoUsername, neoPassword):

        self.gmaps = googlemaps.Client(key=googleKey)
        self.graph = GraphDatabase.driver(uri=url, auth=(neoUsername, neoPassword))
        self.session = self.graph.session()
    
    def get_loc_names(self, lati, longi):

        locs=[]
        places = self.gmaps.reverse_geocode((lati/1e7, longi/1e7))
        for place in places:
            place_type = place['address_components'][0]['types'][0]
            if place_type!='street_number':
                name = place['address_components'][0]['long_name']
                locs.append(name)
        return locs

    def get_nodes(self, query):
        nodes= self.session.run()
        return nodes


url = "bolt://100.25.45.169:33389"
username = "neo4j"
password = "hall-default-sock"
query="MATCH (x) return (x)"

neoGoo = Neo4jGoogleMap(googleKey, username, password)
nodes = neoGoo.get_nodes(query)
#places = neoGeo.get_loc_names(119682336, 84394329)

for node in nodes:
    print(node)
    # longi = node[0]['longitude']
    # lati = node[0]['latitude']
    # locs = map.get_loc(lati, longi)
    # q = "MATCH (x) SET x.location={} return (x)".format(map.get_loc(lati, longi))
    # session.run(q)
    #print(lati, longi)
