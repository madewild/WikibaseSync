# this class makes the correspondence between Wikidata entities and entities in the Wikibase using the external
# identifier for Wikidata

from SPARQLWrapper import SPARQLWrapper, JSON
import configparser


class IdSparql:
    def __init__(self, endpoint, item_identifier, property_identifier):
        self.mapEntity = {}
        self.mapProperty = {}
        self.endpoint = endpoint
        self.item_identifier = item_identifier
        self.property_identifier = property_identifier
        self.app_config = configparser.ConfigParser()
        self.app_config.read('config/application.config.ini')

    def load(self):
        sparql = SPARQLWrapper(self.endpoint)
        query = """
                            select ?item ?id where {
                                ?item <""" + self.app_config.get('wikibase','propertyUri') + """/direct/""" + self.item_identifier + """> ?id
                            }
                        """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results['results']['bindings']:
            split = result['item']['value'].split('/')
            id = split[len(split)-1]
            if id.startswith('Q'):
                self.mapEntity[result['id']['value']] = id
        query = """
                    select ?item ?id where {
                        ?item <""" + self.app_config.get('wikibase','propertyUri') + """/direct/""" + self.property_identifier + """> ?id
                    }
                """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results['results']['bindings']:
            split = result['item']['value'].split('/')
            id = split[len(split) - 1]
            if id.startswith('P'):
                self.mapProperty[result['id']['value']] = id
            else:
                print("This should not happen")

    def get_id(self, id):
        if id.startswith("Q"):
            try:
                return self.mapEntity[id]
            except KeyError:
                print(self.mapEntity)
                raise KeyError(f'Missing mapping for {id}')
        elif id.startswith("P"):
            try:
                return self.mapProperty[id]
            except KeyError:
                print(self.mapProperty)
                raise KeyError(f'Missing mapping for {id}')
        else:
            raise NameError(f'ID does not start with either Q or P: {id}')

    def save_id(self, id, new_id):
        if id.startswith("Q"):
            self.mapEntity[id] = str(new_id)
        elif id.startswith("P"):
            self.mapProperty[id] = str(new_id)
        else:
            raise NameError(f'ID does not start with either Q or P: {id}')

    def contains_id(self,id):
        if id.startswith("Q"):
            return id in self.mapEntity
        elif id.startswith("P"):
            return id in self.mapProperty
        else:
            print('Neither item nor property!')
