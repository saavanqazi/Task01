Upload-validator variants for tests/manifest.json (assertions always live in tests/verifier.json).

A  manifest_A_empty.json    {"task_id", "verifier_configs": []}   <- shipped by default
B  manifest_B_configs.json  verifier_configs = one entry per verifier (name, category, source, assertion)

If the upload rejects A, swap in B and re-zip (no oracle re-run needed: the graders read verifier.json):
    copy /Y local\manifest_variants\manifest_B_configs.json task\tests\manifest.json
    uv run python local\kit.py zip mic-audit-v1.zip
