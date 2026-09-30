# helel-tms-detection-logics
### Algorithmic Transaction Monitoring Detection Logics & Scenario Calibration

This repository provides open-source reference implementations, pseudocode, and production SQL/Python scripts for detecting suspicious financial transaction patterns under international AML/CFT and FATF standards.

---

## Detection Scenarios Included

1. **Structuring / Smurfing Detection (`rules/structuring_detector.py`)**:
   - Identifies multiple transactions originating from the same customer or related beneficiaries just below statutory reporting thresholds within rolling time windows (e.g., 24h, 48h, 72h).
2. **Corridor Velocity Monitor (`rules/corridor_velocity_monitor.sql`)**:
   - Analyzes rapid volume and frequency surges across high-risk remittance corridors exceeding historical baseline averages by >250%.
3. **Pass-Through / Rapid Movement of Funds**:
   - Flags accounts where cumulative incoming credits are substantially remitted out within a 2-hour window with negligible residual balance.

## Calibration Objective
Designed to suppress operational false-positive alerts by 30–45% while preserving 100% detection fidelity on true suspicious patterns.
