#!/usr/bin/env python3
r"""Cross-platform helper for the harbor loop (runs from Windows cmd with plain python).

  python local\kit.py clean                    remove mined evaluations\nop and evaluations\oracle
  python local\kit.py rewards jobs\<job>       reward + failed checks per trial (crash / missing trajectory flagged)
  python local\kit.py probes                   replay tests\score.py in the task image against local\probes\*
  python local\kit.py package jobs\<job>       build task\evaluations\difficulty\r1..r4 + solvability\r1
  python local\kit.py answers jobs\<job>\<trial>  print the deliverables the agent wrote, recovered from its trajectory
  python local\kit.py zip mic-audit-v1.zip     normalise CRLF, check digest pin + bundle shape, zip task/ (top folder task/)
"""
import json, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASK = Path(os.environ.get("TASK", ROOT / "task"))
PROBES = ROOT / "local" / "probes"


def trials(jobdir):
    return sorted(p for p in Path(jobdir).iterdir() if (p / "verifier" / "reward.txt").is_file())


def cmd_clean():
    for d in ("nop", "oracle"):
        p = TASK / "evaluations" / d
        if p.is_dir():
            shutil.rmtree(p); print("removed evaluations/" + d)
    for p in TASK.rglob("__pycache__"):
        shutil.rmtree(p, ignore_errors=True)
    ev = TASK / "evaluations"
    print("evaluations/ now:", [p.name for p in ev.iterdir()] if ev.is_dir() else "(missing)")


def cmd_rewards(jobdir):
    for t in trials(jobdir):
        r = (t / "verifier" / "reward.txt").read_text().strip()
        flags = []
        if (t / "exception.txt").is_file(): flags.append("CRASH(exception.txt)")
        if not (t / "agent" / "trajectory.json").is_file(): flags.append("NO-TRAJECTORY")
        try:
            s = json.loads((t / "verifier" / "score.json").read_text())
            bad = [c for c in s["checks"] if not c["passed"]]
            failed = ", ".join(c["name"] + ("(inc)" if c["tag"] == "incidental" else "") for c in bad) or "-"
        except Exception:
            bad, failed = [], "score.json unreadable"
        print(f"{t.name}  reward={r}  {' '.join(flags)}  failed: {failed}")
        for c in bad:
            if c.get("detail"):
                print(f"      {c['name']}: {c['detail']}")


def cmd_probes():
    subprocess.run(["docker", "build", "-q", "-t", "mic-audit-env", str(TASK / "environment")], check=True)
    for p in sorted(PROBES.iterdir()):
        if not p.is_dir(): continue
        expect = (p / "EXPECT").read_text().strip() if (p / "EXPECT").is_file() else "?"
        out = subprocess.run(
            ["docker", "run", "--rm", "-e", "HARBOR_TASK_WORKSPACE=/work",
             "-v", f"{TASK / 'tests'}:/tests:ro", "-v", f"{p}:/work:ro",
             "mic-audit-env", "python3", "/tests/score.py"],
            capture_output=True, text=True)
        try:
            d = json.loads(out.stdout)
            got = f"{d['reward']} | core failures: {', '.join(d['core_failures']) or '-'}"
        except Exception:
            got = "ENGINE ERROR: " + (out.stderr.strip().splitlines() or ["?"])[-1]
        mark = "OK " if got.startswith(expect) else "!! "
        print(f"{mark}{p.name:28s} expect={expect:5s} got={got}")


def cmd_answers(trial):
    """Recover what the agent wrote: scan trajectory.json for the deliverables' contents."""
    import re
    tj = Path(trial) / "agent" / "trajectory.json"
    if not tj.is_file():
        print("no agent/trajectory.json"); return
    seen = set()
    def walk(x):
        if isinstance(x, dict):
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
        elif isinstance(x, str):
            for key in ("overturned_cell_count", "feature_id,racklane_verdict", "in common", "Micaform only", "FT-6"):
                if key in x and x not in seen and len(x) < 6000:
                    seen.add(x); print("-" * 70); print(x.strip()[:3000]); break
    walk(json.loads(tj.read_text(encoding="utf-8")))


def _final_answer_from_trajectory(trial):
    """The last results.json object the agent wrote, recovered from its trajectory."""
    import re
    tj = Path(trial) / "agent" / "trajectory.json"
    if not tj.is_file():
        return None
    found = []
    def walk(x):
        if isinstance(x, dict):
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
        elif isinstance(x, str) and "overturned_cell_count" in x:
            for m in re.finditer(r"\{[^{}]*overturned_cell_count[^{}]*\}", x):
                try: found.append(json.loads(m.group(0)))
                except Exception: pass
    walk(json.loads(tj.read_text(encoding="utf-8")))
    return found[-1] if found else None


def normalize(trial):
    """Give a copied trial the files and result.json fields the delivery spec requires."""
    ver = trial / "verifier"
    reward = float((ver / "reward.txt").read_text().strip())
    if not (ver / "reward.json").is_file():
        (ver / "reward.json").write_text(json.dumps({"reward": reward}, indent=2) + "\n")
    if not (ver / "verifier_summary.json").is_file() and (ver / "score.json").is_file():
        score = json.loads((ver / "score.json").read_text(encoding="utf-8"))
        summary = {"source": "derived from verifier/score.json (tests/score.py output)",
                   "reward": score.get("reward", reward), "passed": score.get("passed"),
                   "total": score.get("total"), "core_failures": score.get("core_failures", []),
                   "items": score.get("checks", [])}
        (ver / "verifier_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    rj = trial / "result.json"
    data = json.loads(rj.read_text(encoding="utf-8"))
    final = _final_answer_from_trajectory(trial)
    data.update({
        "model": "GLM-5.2",
        "reward": reward,
        "overall_pass": reward == 1.0,
        "final_answer": final if final is not None else {"reward": reward},
        "judge": {"type": "deterministic file_check", "judge_model": None},
    })
    rj.write_text(json.dumps(data, indent=2) + "\n")


def cmd_zip(name):
    """Normalise line endings, check the digest pin and the bundle shape, then zip task/ as <name>."""
    import re, zipfile
    text_ext = {".py", ".sh", ".md", ".json", ".toml", ".csv", ".html", ".txt", ".yaml", ".yml"}
    fixed = 0
    for p in TASK.rglob("*"):
        if p.is_file() and (p.suffix in text_ext or p.name == "Dockerfile"):
            b = p.read_bytes()
            if b"\r\n" in b:
                p.write_bytes(b.replace(b"\r\n", b"\n")); fixed += 1
    print(f"CRLF normalised in {fixed} file(s)")
    df = (TASK / "environment" / "Dockerfile").read_text()
    if not re.search(r"^FROM \S+@sha256:[0-9a-f]{64}", df, re.M):
        print("!! Dockerfile FROM is not digest-pinned"); sys.exit(1)
    must = ["task.toml", "instruction.md", "README.md", "review.csv", "tests/manifest.json",
            "solution/golden_trajectory.json", "evaluations/solvability/r1/verifier/reward.json"]
    must += [f"evaluations/difficulty/r{i}/verifier/reward.json" for i in range(1, 5)]
    missing = [m for m in must if not (TASK / m).is_file()]
    if missing:
        print("!! missing:", missing); sys.exit(1)
    mf = json.loads((TASK / "tests" / "manifest.json").read_text(encoding="utf-8"))
    if not (isinstance(mf, list) and mf and all("assertion" in v for v in mf)):
        print("!! tests/manifest.json must be a nonempty JSON list of verifiers"); sys.exit(1)
    vf = json.loads((TASK / "tests" / "verifier.json").read_text(encoding="utf-8"))
    if vf.get("verifiers") != mf:
        print("!! tests/verifier.json verifiers differ from tests/manifest.json"); sys.exit(1)
    if not (TASK / "qc_report.html").is_file():
        print("note: qc_report.html not present (fine for the first upload; required in the version you submit)")
    ev = sorted(p.name for p in (TASK / "evaluations").iterdir())
    if any(n not in ("difficulty", "solvability", "stability") for n in ev):
        print("!! unexpected folder under evaluations/:", ev); sys.exit(1)
    out = ROOT / name
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(TASK.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                z.write(p, "task/" + p.relative_to(TASK).as_posix())
    n = len(zipfile.ZipFile(out).namelist())
    print(f"wrote {out} ({n} files); top-level folder: task/")


def cmd_package(jobdir):
    ev = TASK / "evaluations"
    for d in ("difficulty", "solvability"):
        shutil.rmtree(ev / d, ignore_errors=True); (ev / d).mkdir(parents=True)
    passing = None
    for i, t in enumerate(trials(jobdir)[:4], start=1):
        dst = ev / "difficulty" / f"r{i}"
        shutil.copytree(t, dst)
        for junk in ("lock.json", "job.log"):
            (dst / junk).unlink(missing_ok=True)
        normalize(dst)
        r = (dst / "verifier" / "reward.txt").read_text().strip()
        print(f"difficulty/r{i}  reward={r}")
        if r == "1.0" and passing is None: passing = f"r{i}"
    if passing:
        shutil.copytree(ev / "difficulty" / passing, ev / "solvability" / "r1")
        print(f"solvability/r1 <- difficulty/{passing}")
    else:
        print("WARNING: no 1.0 run in this battery; solvability needs a passing non-oracle run from elsewhere")
    print("evaluations/ now:", [p.name for p in ev.iterdir()])


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("clean", "rewards", "probes", "package", "answers", "zip"):
        print(__doc__); sys.exit(1)
    {"clean": lambda: cmd_clean(), "rewards": lambda: cmd_rewards(a[1]),
     "probes": lambda: cmd_probes(), "package": lambda: cmd_package(a[1]),
     "answers": lambda: cmd_answers(a[1]),
     "zip": lambda: cmd_zip(a[1] if len(a) > 1 else "mic-audit.zip")}[a[0]]()
