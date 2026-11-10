---
name: aether-privacy-review
description: "Use this skill when you need to decide what may become persistent. It shows the user the candidate material with source, time, and PII or secret hints, records approve, redact, exclude, or purge decisions, and applies redaction to the content that flows downstream. Trigger it before writing any memory file, export, or backup, and whenever the user asks to remove something that was already stored. It never approves material on the user's behalf. For gathering sources use aether-source-intake."
license: MIT
metadata:
  aether-kit-version: "0.2.0"
  aether-skill-version: "1.0"
---

# Privacy review

Make the candidate material understandable so the user can choose what may persist.

## Workflow

1. Present source, time, a minimal preview or safe summary, and any likely secret or PII hint. Detection is advisory; avoid printing the full sensitive value.
2. Record explicit user choices for approve, redact, exclude, or purge. A prior request for a recap does not automatically approve a permanent memory file.
3. Apply redaction to the content handed downstream, not only to the display. Keep rejected material out of recaps when the user excluded it and out of all durable memory, exports, and backup.
4. Recheck eligibility immediately before any file write or external transmission. On a correction or deletion, locate related derived claims and artifacts for removal or rebuild.
5. Verify with distinct synthetic approved and rejected sentinels. Report what was approved, what remains pending, and which downstream artifacts were checked.

## Gotchas

- Redacting only the preview is the most common failure. The downstream record, the memory file, and the export all need the redacted text.
- A deletion in one place leaves derived copies behind: recaps, indexes, summaries, and old archives that quote the removed material.
- Sentinel checks need synthetic material that cannot be confused with real content. Use an unmistakable marker, and confirm it is absent rather than merely unreported.
- A pending item is not a rejected item, but neither is it approved. Both stay out of durable storage until the user answers.

## Guardrails

Never approve private material on the user's behalf. Do not retain deleted payloads in an audit note. The `aether-verification` skill covers a cross-stage exclusion check.
