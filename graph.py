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
            except:
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


googleKey = open('apikey.txt').read()
neoGoo = Neo4jGoogleMap(googleKey, "bolt://3.84.239.221:43863", "neo4j", "curvature-total-lick")
nodes = neoGoo.get_nodes("MATCH (x) return (x)")
neoGoo.update_neo4j_node(nodes, 'location')