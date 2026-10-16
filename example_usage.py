from client import RoktTransactionMomentPostPurchaseOfferArbiter

def main():
    arbiter = RoktTransactionMomentPostPurchaseOfferArbiter()
    tx = {
        "order_total_usd": 150.0,
        "merchant_category": "Luxury Retail",
        "loyalty_tier": "VIP"
    }
    offers = [
        {"offer_id": "r1", "title": "Equinox 1-Month Guest Pass", "cpa_bid_usd": 45.0, "historical_ctr": 0.05, "historical_cvr": 0.12, "is_premium": True},
        {"offer_id": "r2", "title": "$30 Off Uber Eats First Order", "cpa_bid_usd": 22.0, "historical_ctr": 0.06, "historical_cvr": 0.18, "is_premium": False},
        {"offer_id": "r3", "title": "Bargain Discount Outlet", "cpa_bid_usd": 15.0, "min_order_total_usd": 200.0}
    ]
    res = arbiter.arbitrate_offers(tx, offers, slot_capacity=2)
    print("--- Rokt Post-Purchase Offer Arbitration ---")
    print(f"Decision: {res['placement_decision']} | Total Projected eCPM: ${res['projected_slot_ecpm_usd']}")
    for idx, o in enumerate(res['selected_offers'], 1):
        print(f"Slot {idx}: {o['title']} (eCPM: ${o['ecpm_usd']}, Arbitration Score: {o['arbitration_score']})")

if __name__ == "__main__":
    main()
