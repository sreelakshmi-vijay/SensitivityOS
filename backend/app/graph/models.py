from pydantic import BaseModel
from typing import List


class GraphNode(BaseModel):
    id: str
    category: str
    sensitivity: str


class GraphEdge(BaseModel):
    source: str
    target: str
    relationship: str
    weight: float


class SensitivityGraph(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]