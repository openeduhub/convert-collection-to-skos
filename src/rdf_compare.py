from pathlib import PosixPath

from rdflib import Graph, compare
from rdflib.namespace import DCTERMS

from base_logger import logger


def same_graphs(p1: PosixPath, p2: PosixPath) -> bool:
    # second is always second old graph
    g1 = Graph().parse(source=p1)
    g2 = Graph().parse(source=p2)

    iso1 = compare.to_isomorphic(g1)
    iso2 = compare.to_isomorphic(g2)

    _, in_first, in_second = compare.graph_diff(iso1, iso2)

    # compare length
    if len(in_first) > 1:
        logger.info("new graph has more than one change, pushing")
        return False

    if len(in_first) == 1 and len(in_second) == 1:
        # check if just date has changed
        if (None, DCTERMS.modified, None) in in_first and (None, DCTERMS.modified, None) in in_second:
            logger.info("Just date changed, not pushing")
            return True

    logger.info("graphs differ, pushing")
    return
