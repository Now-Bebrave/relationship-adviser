"""Dependency-free calculations for relationship decision templates."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def calculate(data: dict[str, object]) -> dict[str, object]:
    income = float(data.get("monthly_income", 0) or 0)
    essential = float(data.get("essential_expenses", 0) or 0)
    debt = float(data.get("debt_payments", 0) or 0)
    new_debt = float(data.get("new_debt_payment", 0) or 0)
    emergency = float(data.get("emergency_fund", 0) or 0)
    total = essential + debt + new_debt
    remaining = income - total
    return {
        "monthly_commitments": total,
        "remaining_after_commitments": remaining,
        "commitment_ratio": round(total / income, 4) if income else None,
        "emergency_fund_months": round(emergency / total, 2) if total else None,
        "stress": {
            "income_minus_30_percent": round(income * 0.7 - total, 2),
            "income_minus_50_percent": round(income * 0.5 - total, 2),
            "new_support_withdrawn": round(remaining - float(data.get("parent_support", 0) or 0), 2),
        },
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python tools/decision_calculator.py INPUT.json")
        return 2
    result = calculate(json.loads(Path(argv[1]).read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
