"""Offline grocery optimizer: seven Stockholm-area stores, explicit price input and load-aware route planning.
No live prices are scraped or invented. All money is in SEK; distance is supplied by caller.
"""
from dataclasses import dataclass
from functools import lru_cache
from typing import Mapping

STORES = (
    "Willys Sundbyberg Esplanaden", "Lidl Sundbyberg Landsvägen 47",
    "Lidl Solna Bibliotekstorget 2A", "ICA Maxi Solna",
    "ICA Sundbyberg Landsvägen 63", "Hemköp Solna Storgatan 62-64",
    "Hemköp Sundbyberg Mariedalsvägen 9",
)

@dataclass(frozen=True)
class Offer:
    item: str
    store: str
    price_sek: float
    quantity: float = 1.0
    unit_weight_kg: float = 0.0
    member_only: bool = False


def cheapest_basket(shopping: Mapping[str, float], offers: list[Offer], member_stores=frozenset()):
    """Choose lowest total offer per item; caller supplies current validated prices."""
    basket = []
    for item, quantity in shopping.items():
        if quantity <= 0:
            raise ValueError("Quantities must be positive")
        candidates = [o for o in offers if o.item == item and o.quantity > 0 and o.price_sek >= 0
                      and (not o.member_only or o.store in member_stores)]
        if not candidates:
            raise ValueError(f"No eligible price for {item}")
        chosen = min(candidates, key=lambda o: (o.price_sek / o.quantity, o.store))
        basket.append((chosen, quantity, round(chosen.price_sek / chosen.quantity * quantity, 2)))
    return basket


def optimize_route(basket, distances, home="HOME", carry_penalty=0.02):
    """Exact weighted Hamiltonian cycle through chosen stores (max 12 stores).
    Each directed leg incurs distance*(1+carry_penalty*current_kg).
    The basket's selected purchases are picked up at each visited store.
    """
    stops = sorted({offer.store for offer, _, _ in basket})
    if len(stops) > 12: raise ValueError("At most 12 selected stores")
    kg = {s: sum(o.unit_weight_kg * (q / o.quantity) for o, q, _ in basket if o.store == s) for s in stops}
    total_mask = (1 << len(stops)) - 1
    @lru_cache(None)
    def solve(pos, mask):
        if mask == total_mask:
            return (distances[(pos, home)] * (1 + carry_penalty * sum(kg.values())), (home,))
        carried = sum(kg[s] for i, s in enumerate(stops) if mask & (1 << i))
        choices = []
        for i, s in enumerate(stops):
            if not mask & (1 << i):
                tail_cost, tail_route = solve(s, mask | (1 << i))
                choices.append((distances[(pos, s)] * (1 + carry_penalty * carried) + tail_cost,
                                (s,) + tail_route))
        return min(choices)
    score, route = solve(home, 0)
    return {"route": [home, *route], "weighted_distance": round(score, 3),
            "price_sek": round(sum(price for _, _, price in basket), 2),
            "by_store": {s: [o.item for o, _, _ in basket if o.store == s] for s in stops}}
