from fastapi import APIRouter

from app.graph.graph_builder import GraphBuilder

router = APIRouter()


@router.get("/registry/stats")
def registry_stats():

    graph = GraphBuilder.load_graph("../registry")

    return {
        "total_nodes": len(graph.nodes),
        "total_edges": len(graph.edges),
        "nodes": list(graph.nodes)
    }