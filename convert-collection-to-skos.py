import requests
import json
from rdflib import Namespace, Graph, URIRef, SKOS, RDF, DCTERMS, Literal
from rdflib.namespace import SDO
from pprint import pprint

base_url = "https://redaktion.openeduhub.net/edu-sharing/rest/collection/v1/collections/-home-/"
appendix = "/children/collections/"
main_collection_id = "5e40e372-735c-4b17-bbf7-e827a5702b57"
main_collection = {
    "id": main_collection_id,
    "prefLabel": "Main Collection",
    "children": []
}

topic_identifier= [
    "Aktiviert / Sichtbar",
    "activated",
    ""
]

def getRequest(url):
    r = requests.get(url,
                     params={
                         "scope": "MY",
                         "maxItems": "999999",
                         "skipCount": 0,
                         "propertyFilter": "-all-"
                     },
                     headers={
                         "Accept": "application/json"
                     }
                     )
    response = r.json()
    return response


def getCollection(url):
    response = getRequest(url)

    collections = []
    for item in response["collections"]:
        # if item["createdBy"]["firstName"] == "WLO":
        if any(x in topic_identifier for x in item["properties"]["ccm:editorial_state_DISPLAYNAME"]):
            collection = {
                "id": item["ref"]["id"],
                "prefLabel": item["title"],
                "keywords": item.get("properties").get("cclom:general_keyword", []),
                "discipline": item.get("properties").get("ccm:taxonid", ""),
                "educationalContext": item.get("properties").get("ccm:educationalcontext", ""),
                "children": []
            }
        else:
            continue
        collections.append(collection)
    return collections


def get_all_collections(url, parent_collection):
    for collection in getCollection(url):
        print(f"{collection['id']} : {collection['prefLabel']}")
        parent_collection["children"].append(collection)
        get_all_collections(base_url + collection["id"] + appendix, collection)


def getMainCollections(url, collection):
    main_ids = {}
    for collection in getCollection(url):
        main_ids.update({collection['id']: collection['prefLabel']})
    return main_ids


###

start_url = base_url + main_collection_id + appendix

# get all collections
main_ids = getMainCollections(start_url, main_collection)

# add Main collection to main ids
main_ids.update({main_collection_id: "Main-Collection (All)"})

pprint(main_ids)

start_id = input("Which id to convert? ") or main_collection_id
collection_name = main_ids[start_id]
print(f"converting: {collection_name}")

main_collection["id"] = start_id
collection_name = input(
    f"Name of collection (default: {collection_name}): ") or collection_name
print(f"Name: {collection_name}")

url = base_url + start_id + appendix

result_collection: dict = {
    "id": start_id,
    "prefLabel": collection_name,
    "children": []
}

get_all_collections(url, result_collection)


def buildGraph(data):
    g = Graph()
    name = collection_name.lower().replace(" ", "-")
    base_url = URIRef("http://w3id.org/openeduhub/vocabs/oeh-topics/")
    concept_scheme_url = URIRef(
        "http://w3id.org/openeduhub/vocabs/oeh-topics/" + start_id)
    OEHTOPICS = Namespace(base_url)

    g.add((concept_scheme_url, RDF.type, SKOS.ConceptScheme))
    g.add((concept_scheme_url, DCTERMS.creator, Literal(
        "WirLernenOnline Fachportalmanger:innen", lang="de")))
    g.add((concept_scheme_url, DCTERMS.title, Literal(collection_name, lang="de")))

    # get main items and add them as top concepts
    topConcepts = [concept["id"] for concept in data["children"]]

    def parseTree(tree):
        # if id is ConceptScheme, skip
        item_url = base_url + URIRef(tree["id"])
        if tree["id"] == start_id and len(tree["children"]):
            for item in tree["children"]:
                # child_url = URIRef(base_url + item["id"])
                # g.add((base_url, SKOS.narrower, child_url))
                # g.add((child_url, SKOS.broader, base_url))
                parseTree(item)
        else:
            g.add((item_url, RDF.type, SKOS.Concept))
            g.add((item_url, SKOS.prefLabel, Literal(
                tree["prefLabel"], lang="de")))

            if "hiddenLabel" in tree.keys():
                for item in tree["hiddenLabel"]:
                    g.add((item_url, SKOS.hiddenLabel, Literal(item, lang="de")))

            if "keywords" in tree.keys():
                for item in tree["keywords"]:
                    g.add((item_url, SDO.keywords, Literal(item, lang="de")))

            if "discipline" in tree.keys():
                for item in tree["discipline"]:
                    # g.add( (item_url, SDO.about, item))
                    g.add((item_url, SKOS.related, URIRef(item)))

            if tree["id"] in topConcepts:
                g.add((item_url, SKOS.topConceptOf, concept_scheme_url))
                g.add((concept_scheme_url, SKOS.hasTopConcept, item_url))
            else:
                g.add((item_url, SKOS.inScheme, concept_scheme_url))

            if len(tree["children"]):
                for item in tree["children"]:
                    child_url = URIRef(base_url + item["id"])
                    g.add((item_url, SKOS.narrower, child_url))
                    g.add((child_url, SKOS.broader, item_url))
                    parseTree(item)

    parseTree(data)

    g.bind("skos", SKOS),
    g.bind("oeh", OEHTOPICS)
    g.bind("dct", DCTERMS)
    g.bind("sdo", SDO)

    output = g.serialize(format="turtle", base=base_url).decode("utf-8")

    with open("data/graph_" + name + ".ttl", "w") as f:
        f.write(output)


buildGraph(result_collection)
