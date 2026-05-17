from app.graph.graph_builder import GraphBuilder
from app.graph.inference_engine import InferenceEngine

graph = GraphBuilder.load_graph(
    "../registry/core/sensitivity_graph.yaml"
)

entities = [
    "salary",
    "employee_id",
    "tax_id"
]

results = InferenceEngine.escalate_sensitivity(
    graph,
    entities
)

print(results)