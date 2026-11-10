---
name: aether-daily-recap
description: "Use this skill when you need to write a grounded daily or period recap from reviewed structured activity: workstreams, highlights, a timeline, and open loops, with each material claim linked to a source identifier. It separates what the evidence shows from what it suggests and does not invent accomplishments. Trigger it when the user asks what they worked on, how a day or week went, or wants a summary they can share. For raw event normalization use aether-activity-structuring."
license: MIT
metadata:
  aether-kit-version: "0.2.0"
  aether-skill-version: "1.0"
---

# Daily recap

Explain what the approved evidence shows without inventing achievements.

## Workflow

1. Establish the date window and timezone, then read the reviewed structured records. Exclude pending and rejected material.
2. Group related events into workstreams. Write a concise narrative, timeline, and open loops; include highlights only when sources support them.
3. Link each material claim to source identifiers or paths. Mark uncertain context and distinguish a command run from a task completed.
4. Return the recap in chat by default. Write a durable file only when requested, and route any later memory storage through `aether-privacy-review` and `aether-memory`.
5. Check chronology, links, omissions, and a sample of claims against approved sources. Report scope and unresolved questions.

## Gotchas

- Grouping into workstreams is an interpretation. Name the evidence that puts two events in the same stream, and keep singleton work as its own line.
- Highlights are a claim about value. If the sources only show activity, write activity.
- A recap in chat is transient by default. Only a requested file counts as a durable artifact, and even then it is not memory.
- Absence of an open loop is not a closed one. If no source shows a follow-up, report it as unobserved rather than finished.

## Report

Return the date window, the workstreams, the source links behind each material claim, the open loops, the excluded material, and the checks run.
