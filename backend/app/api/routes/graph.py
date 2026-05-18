from pathlib import Path
from fastapi import APIRouter
from app.graph.graph_builder import GraphBuilder

router = APIRouter()

# graph.py lives at backend/app/api/routes/graph.py
# 4 x .parent → backend/, then one more → project root
REGISTRY_PATH = str(Path(__file__).resolve().parent.parent.parent.parent.parent / "registry")

@router.get("/graph")
def get_graph():
    graph = GraphBuilder.load_graph(REGISTRY_PATH)
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
