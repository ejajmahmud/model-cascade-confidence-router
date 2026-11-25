"""Core confidence-based fast-to-frontier model cascade router."""
from typing import Any, Dict


class ModelCascadeRouter:
    """Decides whether a fast model draft is accepted or escalated to a frontier model."""

    HEDGE_PHRASES = ("not sure", "i cannot verify", "might be", "unclear", "unable to determine")

    def __init__(self, confidence_threshold: float = 0.8, fast_cost: float = 1.0, frontier_cost: float = 12.0):
        self.confidence_threshold = confidence_threshold
        self.fast_cost = fast_cost
        self.frontier_cost = frontier_cost
        self.total_routed = 0
        self.escalated_count = 0

    def evaluate_draft(self, output_text: str, confidence: float, valid_schema: bool = True) -> Dict[str, Any]:
        self.total_routed += 1
        low = output_text.lower()
        hedged = any(p in low for p in self.HEDGE_PHRASES)

        escalate = (not valid_schema) or hedged or (confidence < self.confidence_threshold)
        reason = "accepted_fast_draft"
        if not valid_schema:
            reason = "invalid_output_schema"
        elif hedged:
            reason = "hedging_detected"
        elif confidence < self.confidence_threshold:
            reason = "low_confidence"

        if escalate:
            self.escalated_count += 1
            tier = "frontier"
            cost = self.fast_cost + self.frontier_cost
        else:
            tier = "fast"
            cost = self.fast_cost

        return {
            "selected_tier": tier,
            "escalated": escalate,
            "reason": reason,
            "relative_cost": cost,
        }

    def stats(self) -> Dict[str, Any]:
        rate = round(self.escalated_count / max(1, self.total_routed), 4)
        return {"total": self.total_routed, "escalated": self.escalated_count, "escalation_rate": rate}
