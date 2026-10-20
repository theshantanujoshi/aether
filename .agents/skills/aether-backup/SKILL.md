---
name: aether-backup
description: "Plan or perform an optional backup or restore of explicitly approved Aether memory artifacts. Use for encryption, key ownership, restore, retention, or backup deletion. For local memory maintenance use aether-memory."
---

# Optional backup

Back up only user-selected, approved local memory; preserve the ability to restore and delete it.

1. Establish the exact artifacts, destination, retention, and whether the task asks for a design or an actual transfer. Confirm current approval and redaction state.
2. For remote backup, use a maintained authenticated-encryption tool or library chosen for the environment. Keep keys with the user and encrypt before any upload. Describe visible metadata and restore requirements.
3. Do not send pending, rejected, or purged source material. Reconcile restored content against current deletion decisions so an old archive cannot silently revive removed memory.
4. Use synthetic data to check wrong-key rejection, corruption detection, restore, and deletion behavior where an implementation exists. Never call a transport-encrypted upload a client-side encrypted backup.
5. Report what was backed up, location, encryption method, key ownership, checks, and gaps. Do not transfer to a live destination without the user's authorization for that action.
