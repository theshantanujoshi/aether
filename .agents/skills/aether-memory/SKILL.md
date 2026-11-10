---
name: aether-memory
description: "Use this skill when you need to keep user-approved personal activity records in ordinary local files: store the smallest useful record with provenance, answer questions from the stored records, apply corrections, and delete material the user wants gone. It reports where memory lives and proves absence after a deletion. Trigger it when the user asks to save, find, revise, export, or remove persistent records of their activity. For approval use aether-privacy-review; for backup use aether-backup."
license: MIT
metadata:
  aether-kit-version: "0.2.0"
  aether-skill-version: "1.0"
---

# Local memory

Keep persistent memory explicit, inspectable, and reversible.

## Workflow

1. Establish the requested storage location and approved content. Discover existing local memory format rather than assuming a database or vector service exists.
2. Store the smallest useful record with source identifiers, time, content, redaction state, and creation or revision metadata. Use ordinary local files unless the user has chosen another system.
3. Answer search questions from actual stored records. Provide source links and distinguish retrieval from inference. Do not claim semantic search unless the selected repository implements it and a query proves it.
4. Apply correction or deletion across related summaries, indexes, and exports that are in scope. Verify absence with a subsequent search; report inaccessible copies.
5. Check that each persistent record has approval evidence and that rejected or purged material is absent. Use `aether-backup` only when backup is separately requested.

## Gotchas

- Retrieval is not understanding. A keyword match is a lookup; if the answer needs inference, say which record supports it and which part is inferred.
- Deleting the newest file is not deleting a memory. Older notes, recaps, and exports often restate the same fact and need the same treatment.
- A correction changes provenance as well as content. Record who revised it and when, or a later reader cannot tell which version is current.
- Store the smallest useful record. Extra fields that no later question needs become data that later has to be redacted.

## Report

Return the storage path, source coverage, query method, changes made, and the verification result.
