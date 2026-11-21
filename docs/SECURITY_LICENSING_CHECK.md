# Security and licensing check — 21 November 2026

- `uv pip check --python .venv/bin/python`: 133 installed packages checked, no dependency conflicts.
- Source URLs are fixed and reviewed; the HTTPS client rejects local/private DNS addresses, redirects, non-HTML content and responses over 2 MB, and times out after 15 seconds.
- Production extraction is deterministic. HTML is untrusted input; product title, configuration and scoped EGP price must match expected fields. Makers and Ampere visible values must agree with JSON-LD. Text from pages is not used as executable instructions.
- A search for embedded API-key assignments or token-like strings found only environment-variable references and missing-key examples. `.env`, virtual environments, local SQLite and raw supplier captures are excluded from Git and the package.
- Project source is MIT licensed. Third-party pages retain their own rights; Makers explicitly restricts republication, so no raw page material is redistributed. The report includes short factual observations with source links. Dependencies retain their own licenses and are not vendored.
- Supplier robots and terms are linked in `REAL_SOURCING_VALIDATION.md`. No restricted path, cart or checkout was accessed for sourcing.
