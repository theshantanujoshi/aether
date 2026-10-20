---
name: aether-memory
description: "Maintain and search user-approved local Aether memory artifacts with provenance, correction, and deletion. Use when the user asks to save, query, revise, export, or remove persistent personal activity records. For approval use aether-privacy-review."
---

# Local memory

Keep persistent memory explicit, inspectable, and reversible.

1. Establish the requested storage location and approved content. Discover existing local memory format rather than assuming a database or vector service exists.
2. Store the smallest useful record with source identifiers, time, content, redaction state, and creation or revision metadata. Use ordinary local files unless the user has chosen another system.
3. Answer search questions from actual stored records. Provide source links and distinguish retrieval from inference. Do not claim semantic search unless the selected repository implements it and a query proves it.
4. Apply correction or deletion across related summaries, indexes, and exports that are in scope. Verify absence with a subsequent search; report inaccessible copies.
5. Check that each persistent record has approval evidence and that rejected or purged material is absent. Use `aether-backup` only when backup is separately requested.

Do not silently create memory from a transient recap request. Report storage path, source coverage, query method, changes, and verification.
