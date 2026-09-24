#!/usr/bin/env python3
"""Phase 5: make each rollout result.json carry the fields the delivery spec requires.
Usage: python3 local/normalize_results.py task/evaluations/difficulty/r1 [r2 ...]
"""
import json, sys
from pathlib import Path

for arg in sys.argv[1:]:
    trial = Path(arg)
    rj = trial / "result.json"
    data = json.loads(rj.read_text())
    reward = float(json.loads((trial / "verifier" / "reward.json").read_text())["reward"])
    final = {}
    ws = trial / "agent"
    # final_answer: the figures the agent delivered if we can find them, else the reward summary
    for cand in [trial / "artifacts" / "results.json", trial / "results.json"]:
        if cand.is_file():
            final = json.loads(cand.read_text()); break
    data["model"] = "GLM-5.2"
    data["reward"] = reward
    data["overall_pass"] = reward == 1.0
    data["final_answer"] = final or {"reward": reward}
    data["judge"] = {"type": "deterministic", "llm_judge": None,
                     "note": "all checks are deterministic file assertions; no LLM judge in this task"}
    rj.write_text(json.dumps(data, indent=2) + "\n")
    print(f"{trial}: model=GLM-5.2 reward={reward} overall_pass={reward == 1.0}")
