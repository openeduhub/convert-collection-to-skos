from datetime import date, datetime
from pathlib import Path

import requests
from rdflib import DCTERMS, RDF, SKOS, Graph, Literal, Namespace, URIRef
from rdflib.namespace import SDO

from base_logger import logger

class ESConverter:
    base_url = "https://redaktion.openeduhub.net/edu-sharing/rest/collection/v1/collections/-home-/"
    appendix = "/children/collections/"
    main_collection_id = "5e40e372-735c-4b17-bbf7-e827a5702b57"
    main_collection = {
        "id": main_collection_id,
        "prefLabel": "Main Collection",
        "children": []
    }

    # activated will just get collections explicitly activated
    # if empty string also collections not visible 
    # TODO add this to env file
    # deactivated aso fetches collections that are invisible
    editorial_state = [
        "activated",
        "",
        # "deactivated"
    ]

    def getRequest(self, url):
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


    def getCollection(self, url):
        response = self.getRequest(url)
        logger.debug(f"Get collection from {url}")

        collections = []
        try:
            for item in response["collections"]:
                if any(x in self.editorial_state for x in item.get("properties").get("ccm:editorial_state", [])):
                    collection = {
                        "id": item["ref"]["id"],
                        "prefLabel": item["title"],
                        "keywords": item.get("properties").get("cclom:general_keyword", []),
                        "discipline": item.get("properties").get("ccm:taxonid", ""),
                        "educationalContext": item.get("properties").get("ccm:educationalcontext", ""),
                        "description": item.get("properties").get("cm:description", ""),
                        "children": []
                    }
                else:
                    continue
                collections.append(collection)
            return collections
        except KeyError as e:
            logger.error(f"No key \"collections\" in response object. Got keys: {response.keys()}. Url: {url}", e)
            return collections


    def get_all_collections(self, url, parent_collection):
        for collection in self.getCollection(url):
            logger.debug(f"{collection['id']} : {collection['prefLabel']}")
            parent_collection["children"].append(collection)
            self.get_all_collections(self.base_url + collection["id"] + self.appendix, collection)
        return parent_collection


    def getMainCollections(self, url, collection):
        main_ids = {}
        for collection in self.getCollection(url):
            main_ids.update({collection['id']: collection['prefLabel']})
        return main_ids


    def buildGraph(self, data, start_id, collection_name):
        g = Graph()

        name = collection_name
        base_url = URIRef("http://w3id.org/openeduhub/vocabs/oeh-topics/")
        concept_scheme_url = URIRef(
            "http://w3id.org/openeduhub/vocabs/oeh-topics/" + start_id)
        OEHTOPICS = Namespace(base_url)

        g.add((concept_scheme_url, RDF.type, SKOS.ConceptScheme))
        g.add((concept_scheme_url, DCTERMS.creator, Literal(
            "WirLernenOnline Fachportalmanger:innen", lang="de")))
        g.add((concept_scheme_url, DCTERMS.modified, Literal(
            date.today().isoformat()
        )))
        g.add((concept_scheme_url, DCTERMS.title, Literal(collection_name, lang="de")))

        # get main items and add them as top concepts
        topConcepts = [concept["id"] for concept in data["children"]]

        def parseTree(tree):
            # if id is ConceptScheme, skip
            item_url = base_url + URIRef(tree["id"])
            if tree["id"] == start_id and len(tree["children"]):
                for item in tree["children"]:
                    parseTree(item)
            else:
                g.add((item_url, RDF.type, SKOS.Concept))
                g.add((item_url, SKOS.prefLabel, Literal(
                    tree["prefLabel"], lang="de")))
                g.add((item_url, SKOS.notation, Literal(
                    tree["id"])))

                if "hiddenLabel" in tree.keys():
                    for item in tree["hiddenLabel"]:
                        g.add((item_url, SKOS.hiddenLabel, Literal(item, lang="de")))

                if "keywords" in tree.keys():
                    for item in tree["keywords"]:
                        if item != "":
                            g.add((item_url, SDO.keywords, Literal(item, lang="de")))

                if "description" in tree.keys():
                    for item in tree["description"]:
                        if item != "":
                            g.add((item_url, SKOS.definition, Literal(item, lang="de")))

                if "discipline" in tree.keys():
                    for item in tree["discipline"]:
                        g.add((item_url, SKOS.relatedMatch, URIRef(item)))

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

        g.bind("skos", SKOS)
        g.bind("oeh", OEHTOPICS)
        g.bind("dct", DCTERMS)
        g.bind("sdo", SDO)

        # make sure data-directory exists
        Path("data/").mkdir(exist_ok=True)

        filename = f"data/graph_{name}_{datetime.now().isoformat(timespec='seconds')}.ttl"

        g.serialize(destination=filename, format="turtle", base=base_url)

        logger.info(f"Success writing: {filename}")
