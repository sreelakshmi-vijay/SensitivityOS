# SensitivityOS Registry Specification

Each registry YAML file must contain structured definitions for **nodes** and **edges**.

---

## Nodes

Nodes represent entities, concepts, or data elements within a domain.

```yaml
nodes:
  - id: unique_identifier
    category: domain_category
    sensitivity: low | medium | high | critical
```

### Fields

| Field | Description |
|---|---|
| `id` | Unique identifier for the node |
| `category` | Domain-specific classification |
| `sensitivity` | Risk or confidentiality level |

### Sensitivity Levels

| Level | Meaning |
|---|---|
| `low` | Minimal sensitivity |
| `medium` | Moderate sensitivity |
| `high` | Significant sensitivity |
| `critical` | Extremely sensitive or regulated |

---

## Edges

Edges define semantic relationships between nodes.

```yaml
edges:
  - source: node_a
    target: node_b
    relationship: semantic_relationship
    weight: 0.0-1.0
```

### Fields

| Field | Description |
|---|---|
| `source` | Origin node ID |
| `target` | Destination node ID |
| `relationship` | Type of semantic connection |
| `weight` | Confidence score between `0.0` and `1.0` |

---

## Example Registry

```yaml
nodes:
  - id: customer_email
    category: pii
    sensitivity: high

  - id: billing_record
    category: finance
    sensitivity: critical

edges:
  - source: customer_email
    target: billing_record
    relationship: linked_to
    weight: 0.92
```

---

## Principles

### Domain-Specific Registries

Registries should focus on a clearly defined domain or context.

### Explainable Relationships

All relationships must be interpretable and semantically meaningful.

### Confidence-Based Weighting

Weights represent confidence, relevance, or strength of association.

### Community Contributions

The specification encourages collaborative extension and improvement by the community.