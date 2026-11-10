# Aether capability map

| Capability | Skill | Agent |
| --- | --- | --- |
| Cross-stage activity workflow | `aether-workflow` | `aether_coordinator` |
| Source selection and provenance | `aether-source-intake` | `aether_source_steward` |
| Human approval and redaction | `aether-privacy-review` | `aether_privacy_reviewer` |
| Structured activity records | `aether-activity-structuring` | `aether_structurer` |
| Grounded daily narrative | `aether-daily-recap` | `aether_synthesizer` |
| Persistent local memory and search | `aether-memory` | `aether_memory_curator` |
| Optional backup and restore | `aether-backup` | `aether_backup_specialist` |
| Repository file inventory | `aether-repository-inventory` | `aether_repository_mapper` |
| Source-backed graph relationships | `aether-repository-relations` | `aether_relation_analyst` |
| Interactive local 3D graph | `aether-repository-graph-3d` | `aether_graph_renderer` |
| Output and privacy verification | `aether-verification` | `aether_verifier` |

The kit provides workflows, not a prebuilt activity-memory runtime. Read each skill's scope before selecting it. The graph renderer is a support script that produces an on-demand local artifact.

## Skill folders

Each skill is a portable folder under `.agents/skills/`:

```
aether-<name>/
├── SKILL.md                       # frontmatter and instructions
├── references/                    # optional detail loaded on demand
├── scripts/                       # optional executable helpers
├── assets/                        # optional templates and static resources
└── evals/
    ├── evals.json                 # behavior cases with expected output and assertions
    └── trigger-queries.json       # prompts labeled should_trigger or not
```

`evals/evals.json` covers what the skill should produce; `evals/trigger-queries.json` covers when the skill should load, including near-misses that need a different skill. `python scripts/validate_evals.py` reports the coverage of both sets.
