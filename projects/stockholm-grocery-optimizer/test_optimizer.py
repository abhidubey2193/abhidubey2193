import unittest
from optimizer import Offer, cheapest_basket, optimize_route, STORES

class TestOptimizer(unittest.TestCase):
    def test_exact_store_count(self):
        self.assertEqual(len(STORES), 7)
    def test_member_exclusion(self):
        offers = [Offer("milk", "A", 9, member_only=True), Offer("milk", "B", 12)]
        self.assertEqual(cheapest_basket({"milk": 1}, offers)[0][0].store, "B")
    def test_cheapest_unit_price(self):
        basket = cheapest_basket({"milk": 2}, [Offer("milk", "A", 20, 2), Offer("milk", "B", 12)])
        self.assertEqual(basket[0][2], 20)
    def test_route(self):
        basket = cheapest_basket({"milk": 1}, [Offer("milk", "A", 10, 1, 1)])
        result = optimize_route(basket, {("HOME", "A"): 2, ("A", "HOME"): 3})
        self.assertEqual(result["route"], ["HOME", "A", "HOME"])
        self.assertEqual(result["price_sek"], 10)
if __name__ == "__main__": unittest.main()
