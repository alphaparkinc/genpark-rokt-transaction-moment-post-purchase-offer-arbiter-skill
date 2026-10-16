#!/usr/bin/env python3
import json
import sys
from client import RoktTransactionMomentPostPurchaseOfferArbiter

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        arbiter = RoktTransactionMomentPostPurchaseOfferArbiter()
        tx = {"order_total_usd": 125.0, "merchant_category": "Apparel", "loyalty_tier": "VIP"}
        offers = [
            {"offer_id": "rokt_1", "title": "$25 Off HelloFresh", "cpa_bid_usd": 20.0, "historical_ctr": 0.04, "historical_cvr": 0.15, "is_premium": False},
            {"offer_id": "rokt_2", "title": "Complimentary WSJ 3-Month Access", "cpa_bid_usd": 35.0, "historical_ctr": 0.03, "historical_cvr": 0.12, "is_premium": True},
            {"offer_id": "rokt_3", "title": "Casino Spin Bonus", "cpa_bid_usd": 50.0, "excluded_merchant_categories": ["Apparel"]}
        ]
        res = arbiter.arbitrate_offers(tx, offers, slot_capacity=2)
        assert len(res["selected_offers"]) == 2
        assert res["placement_decision"] == "RENDER_TRANSACTION_MOMENT_WIDGET"
        print(f"[TEST PASS] Rokt Offer Arbiter Passed! Projected eCPM: ${res['projected_slot_ecpm_usd']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-rokt-arbiter", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "arbitrate_offers", "description": "Rokt post-purchase transaction moment offer arbiter"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                arbiter = RoktTransactionMomentPostPurchaseOfferArbiter()
                out = arbiter.arbitrate_offers(args.get("transaction_context", {}), args.get("candidate_offers", []), args.get("slot_capacity", 2))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
