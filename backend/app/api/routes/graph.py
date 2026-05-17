from fastapi import APIRouter

from app.graph.graph_builder import GraphBuilder

router = APIRouter()


@router.get("/graph")
def get_graph():

    graph = GraphBuilder.load_graph("../registry")

    nodes = []
    edges = []

    for node, data in graph.nodes(data=True):

        nodes.append({
            "id": node,
            "label": node,
            "sensitivity": data.get("sensitivity")
        })

    for source, target, data in graph.edges(data=True):

        edges.append({
            "from": source,
            "to": target,
            "label": data.get("relationship"),
            "weight": data.get("weight")
        })

    return {
        "nodes": nodes,
        "edges": edges
    }