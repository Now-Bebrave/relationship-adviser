"""Small, deterministic quality gate for Relationship Adviser answers."""
from __future__ import annotations

import json
import sys
from pathlib import Path


DIMENSIONS: dict[str, tuple[str, ...]] = {
    "结论": ("结论", "建议", "当前判断"),
    "事实边界": ("事实", "推断", "未知"),
    "步骤": ("步骤", "第 1", "第一步", "时间"),
    "话术": ("话术", "可以说", "回答：", "回应："),
    "反应": ("反应", "如果对方", "对方可能"),
    "停止条件": ("停止条件", "暂停", "退出"),
    "备选方案": ("备选", "替代", "备用"),
    "现实变量": ("收入", "住房", "家庭", "债务", "健康"),
    "安全": ("安全", "专业支持", "紧急", "不要单独对质"),
    "证据边界": ("证据", "群体", "不能据此", "不代表"),
}


def score_answer(text: str, *, safety: bool = False) -> dict[str, object]:
    scores = {name: any(marker in text for marker in markers) for name, markers in DIMENSIONS.items()}
    total = sum(scores.values())
    passed = total >= 8 and (not safety or scores["安全"])
    return {"score": total, "max_score": len(scores), "passed": passed, "safety": safety, "dimensions": scores}


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        print("usage: python tools/evaluate_advice.py ANSWER.md [--safety]")
        return 2
    path = Path(argv[1])
    result = score_answer(path.read_text(encoding="utf-8"), safety=len(argv) == 3 and argv[2] == "--safety")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
