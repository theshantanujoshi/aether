---
name: aether-privacy-review
description: "Apply Aether's human review boundary before activity becomes persistent memory, an export, or a backup. Use for approval, redaction, exclusion, and purge decisions. For source gathering use aether-source-intake."
---

# Privacy review

Make the candidate material understandable so the user can choose what may persist.

1. Present source, time, a minimal preview or safe summary, and any likely secret or PII hint. Detection is advisory; avoid printing the full sensitive value.
2. Record explicit user choices for approve, redact, exclude, or purge. A prior request for a recap does not automatically approve a permanent memory file.
3. Apply redaction to the content handed downstream, not only to the display. Keep rejected material out of recaps when the user excluded it and out of all durable memory, exports, and backup.
4. Recheck eligibility immediately before any file write or external transmission. On a correction or deletion, locate related derived claims and artifacts for removal or rebuild.
5. Verify with distinct synthetic approved and rejected sentinels. Report what was approved, what remains pending, and which downstream artifacts were checked.

Never approve private material on the user's behalf. Do not retain deleted payloads in an audit note. The `aether-verification` skill covers a cross-stage exclusion check.
