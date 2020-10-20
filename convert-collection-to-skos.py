import requests
import json
from rdflib import Namespace, Graph, URIRef, SKOS, RDF, DCTERMS, Literal

base_url = "https://redaktion.openeduhub.net/edu-sharing/rest/collection/v1/collections/-home-/"
appendix = "/children/collections/"
main_collection_id = "5e40e372-735c-4b17-bbf7-e827a5702b57"
main_collection = {
    "id": main_collection_id,
    "prefLabel": "Main Collection",
    "children": []
}

def getRequest(url):
    r = requests.get(url,
                     params = {
                         "scope":"MY",
                         "maxItems":"999999",
                         "skipCount": 0,
                         "propertyFilter": "-all-"
                     },
                     headers = {
                         "Accept": "application/json"
                     }
    )
    response = r.json()
    return response

def getCollection(url):
    response = getRequest(url)

    collections = []
    for item in response["collections"]:
        collection = {
            "id": item["ref"]["id"],
            "prefLabel": item["title"],
            "keywords": item.get("properties").get("cclom:general_keyword", []),
            "discipline": item.get("properties").get("ccm:taxonid_DISPLAYNAME", ""),
            "children": []
        }
        collections.append(collection)
    return collections

def get_all_collections(url, parent_collection):
    for collection in getCollection(url):
        print(f"{collection['id']} : {collection['prefLabel']}")
        parent_collection["children"].append(collection)
        get_all_collections(base_url + collection["id"] + appendix, collection)

start_id = input("Which id to convert? ") or main_collection_id
print(f"converting: {start_id}")

main_collection["id"] = start_id
main_collection["prefLabel"] = input("Name of collection: ") or main_collection["prefLabel"]
print(f"Name: {main_collection['prefLabel']}")

url = base_url + start_id + appendix
get_all_collections(url, main_collection)

with open("output.json", "w") as outfile:
    json.dump(main_collection, outfile)

def buildGraph(data):
    g = Graph()
    name = "oeh-topics"
    base_url = URIRef("http://w3id.org/openeduhub/vocabs/oeh-topics/")
    OEHTOPICS = Namespace(base_url)

    g.add((base_url, RDF.type, SKOS.ConceptScheme))
    g.add( (base_url, DCTERMS.creator, Literal("WirLernenOnline Fachportalmanger:innen", lang="de")))

    # get main items and add them as top concepts
    topConcepts = [concept["id"] for concept in data["children"]]

    def parseTree(tree):
        item_url = base_url + URIRef(tree["id"])

        g.add( (item_url, RDF.type, SKOS.Concept) )
        g.add( (item_url, SKOS.prefLabel, Literal(tree["prefLabel"], lang="de")))

        if "hiddenLabel" in tree.keys():
            for item in tree["hiddenLabel"]:
                g.add( (item_url, SKOS.hiddenLabel, Literal(item, lang="de")))

        if tree["id"] in topConcepts:
            g.add( (item_url, SKOS.topConceptOf, base_url) )
            g.add( (base_url, SKOS.hasTopConcept, item_url) )
        else:
            g.add( (item_url, SKOS.inScheme, base_url) )

        if len(tree["children"]):
            for item in tree["children"]:
                child_url = URIRef(base_url + item["id"])
                g.add( (item_url, SKOS.narrower, child_url))
                g.add( (child_url , SKOS.broader, item_url))
                parseTree(item)

    parseTree(data)

    g.bind("skos", SKOS),
    g.bind("oeh", OEHTOPICS)
    g.bind("dct", DCTERMS)

    output = g.serialize(format="turtle", base=base_url).decode("utf-8")

    with open("graph.ttl", "w") as f:
        f.write(output)

buildGraph(main_collection)
