from app.graph.graph_builder import GraphBuilder
from app.graph.inference_engine import InferenceEngine
from pathlib import Path

REGISTRY_PATH = str(Path(__file__).resolve().parent.parent / "registry")

graph = GraphBuilder.load_graph(REGISTRY_PATH)

print(f"Graph loaded: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
print("Nodes:", list(graph.nodes))

entities = [n for n in ["salary", "employee_id", "tax_id", "patient_id", "bank_account"] if n in graph.nodes]

results = InferenceEngine.escalate_sensitivity(graph, entities)

for entity, result in results.items():
    print(f"\n{entity}: {result['base_sensitivity']} -> {result['final_sensitivity']}")
    for r in result["reasoning"]:
        print(f"  {r['relationship']} -> {r['connected_entity']} (weight={r['weight']}, escalated={r['triggered_escalation']})")
