from pathlib import Path
from fastapi import APIRouter
from app.graph.graph_builder import GraphBuilder

router = APIRouter()

# registry.py lives at backend/app/api/routes/registry.py
# 4 x .parent → backend/, then one more → project root
REGISTRY_PATH = str(Path(__file__).resolve().parent.parent.parent.parent.parent / "registry")

@router.get("/registry/stats")
def registry_stats():
    graph = GraphBuilder.load_graph(REGISTRY_PATH)
    return {
        "total_nodes": len(graph.nodes),
        "total_edges": len(graph.edges),
        "nodes": list(graph.nodes)
    }
