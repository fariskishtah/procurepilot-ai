# Real sourcing validation

## Primary laptop scenario

NileTech Operations' original 10-laptop, 300,000 EGP request remains unverified. No Tavily key is available. We did not obtain a permitted, complete laptop supplier feed with RAM, storage, warranty, price, stock, tax, and delivery evidence. The project makes no laptop recommendation.

## Secondary electronics scenario

A separate fictional NileTech R&D request compares 10 HC-05 wireless serial modules, budget 3,000 EGP. The source is the public product page at https://makhzan.merope.dev/products/b8c70b58-ff9c-406e-8d22-e256089ce7ca-hc-05-bluetooth-module-serial-ttl. This is a catalog/aggregator observation, not a direct quote from each shop. The page links to the underlying suppliers and reports when each offer was last checked. Its terms permit search and comparison and restrict automated access beyond robots guidance: https://makhzan.merope.dev/terms. Its robots.txt disallows `/search` and `/api/` but does not disallow the reviewed `/products/` page: https://makhzan.merope.dev/robots.txt. The adapter fetches only that exact reviewed page, once per run, with a timeout and size limit. No raw page capture is redistributed.

The current offers are parsed from the page's visible `Offers` list. The separate stale-offer disclosure is excluded. Every accepted offer has a supplier, a title, an EGP price, a supplier link, the catalog URL, a retrieval timestamp, the page's relative checked-time text, a short price evidence excerpt and a SHA-256 of the fetched HTML. The checked-time text is relative and is not converted into a fabricated exact timestamp.

One direct supplier page (Makers Electronics) was manually checked in a browser and showed the same 195 EGP price and in-stock statement at https://makerselectronics.com/product/hc-05-bluetooth-module-3-3v/. Its robots.txt welcomes AI search/assistant crawlers on product pages. Other direct supplier pages returned 403 in browser retrieval, and the project does not bypass that. The catalog's AI product matching may be wrong. Shipping, tax, warranty and bulk availability are unknown. All offers remain `needs_verification`; a price-only order is provided for comparison, not a purchasing recommendation.

The earlier candidate `nicheiqs.com` CC BY dataset was inspected and rejected for this scenario: it contained only two laptop-related rows, including a laptop stand, and at least one price/currency combination appeared implausible. Pricelists.org's documented unauthenticated search API returned empty offers for three trial queries. Neither source is used to fabricate offers.
