from neo4j import GraphDatabase
import googlemaps

class Neo4jGoogleMap:

    def __init__(self, googleapi, bolt_url, neoUsername, neoPassword):

        self.gmaps = googlemaps.Client(key=googleapi)
        self.graph = GraphDatabase.driver(uri=bolt_url, auth=(neoUsername, neoPassword))
        self.session = self.graph.session()
    
    def get_loc_names(self, lati, longi):

        locs=[]
        places = self.gmaps.reverse_geocode((lati, longi))
        for place in places:
            try:
            
                place_type = place['address_components'][0]['types'][0]
                if place_type!='street_number':
                    name = place['address_components'][0]['long_name']
                    locs.append(name)
            except IndexError:
                pass
        return locs

    def get_nodes(self, query):
        nodes= self.session.run(query)
        return nodes
		
    def update_neo4j_node(nodes, new_value):
        longi = node[0]['longitude']
        lati  = node[0]['latitude']
        for node in nodes:
            if longi and lati:
                geoloc = self.get_loc_names(lati, longi)
                q= "MATCH (x) x.{}={} return (x)".format(new_value, geoloc)
                self.session.run(q)

url = "bolt://3.84.239.221:43863"
googleKey = open('apikey.txt').read()
username = "neo4j"
password = "curvature-total-lick"
query="MATCH (x) return (x)"

neoGoo = Neo4jGoogleMap(googleKey, url, username, password)
nodes = neoGoo.get_nodes(query)
#places = neoGeo.get_loc_names(119682336, 84394329)

for node in nodes:
    longi = node[0]['longitude']
    lati = node[0]['latitude']
    if longi and lati:
        geoloc = neoGoo.get_loc_names(lati,longi)
        #print(longi, lati, geoloc)
        # locs = map.get_loc(lati, longi)
        q = "MATCH (x) SET x.location={} return (x)".format(geoloc)
        #print(q)
        neoGoo.session.run(q)
    #print(lati, longi)