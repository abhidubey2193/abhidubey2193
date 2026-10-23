# Stockholm Grocery Optimizer 🛒

**Status:** Offline Python reference implementation, not the earlier full FastAPI application and not a live-price service.

Compare an explicit shopping list across **exactly seven** stores in Sundbyberg and Solna. Choose the lowest eligible unit price (including membership rules), prepare store-wise purchases, and find an exact, load-aware round trip using caller-supplied walking/driving distances.

## Capabilities
- Seven configured stores, no Coop
- Price-per-unit comparison and cheapest-item selection
- Member-only price eligibility
- Explicit quantities and item weights
- Exact route optimization using dynamic programming; cost penalizes carrying heavier bags
- Store-wise shopping list and basket cost

**Safety and accuracy:** This code does not query current supermarket prices or road networks. Provide verified price offers and a distance matrix. A real production application needs licensed price sources, addresses/geocoding and checkout UI. The shopping choice is independently cheapest per item; optimizing combined price-plus-travel cost remains future work.

## Test
```bash
cd projects/stockholm-grocery-optimizer
python -m unittest discover -p 'test_*.py' -v
```

Earlier work included a larger FastAPI prototype. This public extract is a small standalone implementation rebuilt for demonstration rather than a copy of the earlier archive.
