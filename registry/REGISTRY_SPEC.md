# SensitivityOS Registry Specification

Each registry YAML file must contain structured definitions for **nodes** and **edges**.
Files may use either the `.yaml` or `.yml` extension — both are loaded automatically.

---

## Nodes

Nodes represent data concepts, fields, or entity types within a domain.

```yaml
nodes:
  - id: unique_identifier
    category: domain_category
    sensitivity: public | internal | confidential | restricted
```

### Sensitivity Tiers

| Tier | Meaning | Regulatory Examples |
|---|---|---|
| `public` | No restrictions; safe to share openly | N/A |
| `internal` | Staff-only; low risk if disclosed internally | General governance |
| `confidential` | Need-to-know; significant risk if exposed | GDPR Art. 5, CCPA |
| `restricted` | Regulated data; legal risk if exposed | GDPR Art. 9, HIPAA, PCI-DSS |

---

## Edges

Edges define semantic relationships between nodes that drive sensitivity escalation.

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
| `relationship` | Semantic relationship type (e.g. `implies_phi`, `escalates_financial_sensitivity`) |
| `weight` | Confidence score 0.0–1.0. Escalation only fires at weight ≥ 0.8 |

### Relationship Types

| Type | Meaning |
|---|---|
| `implies_phi` | Source field implies the presence of PHI when co-located with target |
| `escalates_financial_sensitivity` | Source elevates financial sensitivity of target |
| `strongly_escalates` | High-confidence escalation (use weight ≥ 0.90) |
| `hr_escalation` | HR-domain sensitivity escalation |
| `re_identifies` | Source can re-identify an individual when combined with target |
| `pci_scope` | Source brings target into PCI-DSS scope |
| `financial_exposure` | Source creates financial exposure for target |
| `identifies_subject` | Source uniquely identifies the data subject |

---

## Example Registry

```yaml
nodes:
  - id: customer_email
    category: pii
    sensitivity: confidential

  - id: billing_record
    category: finance
    sensitivity: restricted

edges:
  - source: customer_email
    target: billing_record
    relationship: identifies_subject
    weight: 0.92
```

---

## Principles

- **Domain-specific registries** should focus on a clearly defined domain.
- **Explainable relationships** must be semantically meaningful and human-readable.
- **Confidence-based weighting** — weights represent strength of association.
- **Human feedback updates weights** — reviewer corrections are written back to registry files.