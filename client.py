"""
Rokt-inspired Post-Purchase Transaction Moment Offer Arbiter (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import math
import random
from typing import Dict, Any, List

class RoktTransactionMomentPostPurchaseOfferArbiter:
    def __init__(self, platform_name: str = "GenPark-Rokt-Yield-Arbiter"):
        self.platform_name = platform_name

    def compute_ecpm_yield(self, offer: Dict[str, Any]) -> float:
        # eCPM = CTR * CVR * CPA * 1000
        ctr = float(offer.get("historical_ctr", 0.02))
        cvr = float(offer.get("historical_cvr", 0.10))
        cpa = float(offer.get("cpa_bid_usd", 15.0))
        ecpm = ctr * cvr * cpa * 1000.0
        return round(ecpm, 2)

    def evaluate_brand_suitability(self, offer: Dict[str, Any], context: Dict[str, Any]) -> bool:
        restricted_cats = set(offer.get("excluded_merchant_categories", []))
        order_cat = context.get("merchant_category", "")
        if order_cat in restricted_cats:
            return False
        # Minimum basket size requirement
        order_total = float(context.get("order_total_usd", 0.0))
        min_basket = float(offer.get("min_order_total_usd", 0.0))
        if order_total < min_basket:
            return False
        return True

    def arbitrate_offers(self, transaction_context: Dict[str, Any], candidate_offers: List[Dict[str, Any]], slot_capacity: int = 2) -> Dict[str, Any]:
        eligible_offers = []
        for o in candidate_offers:
            if not self.evaluate_brand_suitability(o, transaction_context):
                continue
            ecpm = self.compute_ecpm_yield(o)
            
            # Epsilon-greedy exploration / exploitation
            # Contextual score = eCPM * affinity_multiplier
            affinity = 1.2 if transaction_context.get("loyalty_tier") == "VIP" and o.get("is_premium") else 1.0
            arbitrated_score = round(ecpm * affinity, 2)
            eligible_offers.append({**o, "ecpm_usd": ecpm, "arbitration_score": arbitrated_score})
            
        eligible_offers.sort(key=lambda x: x["arbitration_score"], reverse=True)
        selected = eligible_offers[:slot_capacity]
        
        total_projected_ecpm = sum(x["ecpm_usd"] for x in selected)
        return {
            "arbiter": self.platform_name,
            "transaction_order_total": transaction_context.get("order_total_usd", 0.0),
            "total_candidates_screened": len(candidate_offers),
            "eligible_candidates": len(eligible_offers),
            "selected_offers": selected,
            "projected_slot_ecpm_usd": round(total_projected_ecpm, 2),
            "placement_decision": "RENDER_TRANSACTION_MOMENT_WIDGET" if selected else "SUPPRESS_MOMENT_TO_PROTECT_UX"
        }
