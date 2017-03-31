import os
import rdflib

from rdflib import plugin
from string import Template

def lookup(concept):
    plugin.register(
                'sparql', rdflib.query.Processor,
                'rdfextras.sparql.processor', 'Processor')
    plugin.register(
                'sparql', rdflib.query.Result,
                'rdfextras.sparql.query', 'SPARQLQueryResult')

    dirname = os.getcwd()
    sentic_local = os.path.join(dirname, "senticnet2.rdf.xml")
    parsed_graph = rdflib.Graph().parse(sentic_local, format="xml")
    query_base = ('PREFIX sentic: <http://sentic.net/api/> '\
                    'SELECT ?pleasantness ?attention ?sensitivity ?aptitude '\
                    'WHERE { '\
                    '?concept sentic:text "$concept"; '\
                    'sentic:pleasantness ?pleasantness; '\
                    'sentic:attention ?attention; '\
                    'sentic:sensitivity ?sensitivity; '\
                    'sentic:aptitude ?aptitude. '\
                    '}')

    query_str = query_base.replace("concept" , concept)
    query = parsed_graph.query(str(query_str))
    if len(query) == 0:
        return None
    return dict((str(sentic), float(score)) for (sentic, score) in query._get_bindings()[0].iteritems())

lookup('love')