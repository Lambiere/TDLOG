
# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """
SELECT DISTINCT ?countryLabel ?capitalLabel ?population ?continentLabel ?presidentLabel ?flag
WHERE
{
  ?country wdt:P31 wd:Q3624078;
           wdt:P1082 ?population;
           wdt:P30 ?continent
  #not a former country
  FILTER NOT EXISTS {?country wdt:P31 wd:Q3024240}
  #and no an ancient civilisation (needed to exclude ancient Egypt)
  FILTER NOT EXISTS {?country wdt:P31 wd:Q28171280}
  OPTIONAL { ?country wdt:P36 ?capital } .
  OPTIONAL { ?country wdt:P35 ?president} .
  OPTIONAL { ?country wdt:P41 ?flag} .

  SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
}
ORDER BY ASC(?continentLabel)"""


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result)

import urllib.request

urllib.request.urlretrieve(results["results"]["bindings"][140]['flag']['value'], "local-filename.jpg")