from neo4j import GraphDatabase
import googlemaps

class Neo4jGoogleMap:

    def __init__(self, googleapi, bolt_url, neoUsername, neoPassword):

        self.gmaps = googlemaps.Client(key=googleapi)
        self.graph = GraphDatabase.driver(uri=bolt_url, auth=(neoUsername, neoPassword))
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
        nodes= self.session.run(query)
        return nodes


url = "bolt://100.27.2.160:33349"
googleKey = open('../../api.txt').read()
username = "neo4j"
password = "dares-warnings-pound"
query="MATCH (x) return (x)"

neoGoo = Neo4jGoogleMap(googleKey, url, username, password)
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