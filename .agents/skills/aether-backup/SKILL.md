---
name: aether-backup
description: "Use this skill when the user asks for an optional backup or restore of explicitly approved memory artifacts: choose the payload and destination, keep keys with the user, encrypt before any remote transfer, and confirm that an old archive cannot revive deleted material. Trigger it when the user wants to copy, archive, snapshot, or restore their Aether memory, or to design that policy before implementing it. It never transfers to a live destination without authorization. For everyday memory upkeep use aether-memory."
license: MIT
metadata:
  aether-kit-version: "0.2.0"
  aether-skill-version: "1.0"
---

# Optional backup

Back up only user-selected, approved local memory; preserve the ability to restore and delete it.

## Workflow

1. Establish the exact artifacts, destination, retention, and whether the task asks for a design or an actual transfer. Confirm current approval and redaction state.
2. For remote backup, use a maintained authenticated-encryption tool or library chosen for the environment. Keep keys with the user and encrypt before any upload. Describe visible metadata and restore requirements.
3. Do not send pending, rejected, or purged source material. Reconcile restored content against current deletion decisions so an old archive cannot silently revive removed memory.
4. Use synthetic data to check wrong-key rejection, corruption detection, restore, and deletion behavior where an implementation exists. Never call a transport-encrypted upload a client-side encrypted backup.
5. Report what was backed up, location, encryption method, key ownership, checks, and gaps. Do not transfer to a live destination without the user's authorization for that action.

## Gotchas

- A transport-encrypted upload is not a client-side encrypted backup. The upload channel is not the same as encryption at rest under a key the user holds.
- Backups inherit deleted content. If memory was purged after the last snapshot, restoring that snapshot resurrects it, so reconcile before every restore.
- Losing the key loses the backup. Keep the key with the user and state the restore requirements with the artifact.
- Filenames and archive listings leak. A backup of personal notes can reveal project and client names even when the content is encrypted.

## Report

Return the payload, destination, retention, encryption method, key ownership, restore and deletion checks, and the gaps that remain unverified.
