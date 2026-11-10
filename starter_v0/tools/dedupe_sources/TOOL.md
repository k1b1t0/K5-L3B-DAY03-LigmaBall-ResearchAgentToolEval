---
name: dedupe_sources
track: core
kind: local_formatter
provider: None
requires_env: []
inputs: [items]
outputs: [items, input_count, item_count, duplicates_removed]
side_effect: false
---

# Deduplicate research sources

Removes duplicate research items by normalized HTTP(S) URL and preserves the first copy. It ignores URL fragments and common tracking parameters such as `utm_*` and `fbclid`, while preserving meaningful query parameters. Use it after combining search results from multiple sources and before formatting a digest. Invalid input returns an error object instead of raising.
