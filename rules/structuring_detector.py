#!/usr/bin/env python3
"""
HELEL Oversight & Compliance Advisory
Rule 101: Structuring & Smurfing Detection Engine
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any

class StructuringDetector:
    def __init__(self, threshold_limit: float = 10000.0, proximity_margin: float = 0.15, window_hours: int = 48, min_count: int = 2):
        self.threshold_limit = threshold_limit
        self.min_single_amount = threshold_limit * (1.0 - proximity_margin)
        self.window_delta = timedelta(hours=window_hours)
        self.min_count = min_count

    def analyze_transactions(self, customer_id: str, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        suspicious_batches = []
        sub_threshold_txns = [
            t for t in transactions 
            if self.min_single_amount <= t['amount'] < self.threshold_limit
        ]
        sub_threshold_txns.sort(key=lambda x: x['timestamp'])

        for i, base_txn in enumerate(sub_threshold_txns):
            window_txns = [base_txn]
            for candidate in sub_threshold_txns[i+1:]:
                if candidate['timestamp'] - base_txn['timestamp'] <= self.window_delta:
                    window_txns.append(candidate)
            
            total_window_val = sum(t['amount'] for t in window_txns)
            if len(window_txns) >= self.min_count and total_window_val >= self.threshold_limit:
                suspicious_batches.append({
                    "customer_id": customer_id,
                    "alert_type": "STRUCTURING_BELOW_REPORTING_THRESHOLD",
                    "transaction_count": len(window_txns),
                    "total_amount": round(total_window_val, 2),
                    "window_start": window_txns[0]['timestamp'].isoformat(),
                    "window_end": window_txns[-1]['timestamp'].isoformat(),
                    "action_required": "Initiate EDD & Evaluate for STR/SAR Escalation"
                })
        return suspicious_batches

if __name__ == "__main__":
    detector = StructuringDetector(threshold_limit=10000, proximity_margin=0.15, window_hours=48)
    sample_data = [
        {"id": "TX101", "amount": 9500.0, "timestamp": datetime(2026, 9, 28, 10, 0)},
        {"id": "TX102", "amount": 9800.0, "timestamp": datetime(2026, 9, 29, 14, 30)},
    ]
    alerts = detector.analyze_transactions("CUST_88219", sample_data)
    print(f"Generated {len(alerts)} alerts: {alerts}")
