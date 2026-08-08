# Sandbox report — synapse-e5-import

- domain: `synapse_import`
- seed: `0`
- primary (`accuracy`): **0.8636**
- accuracy: `0.8636`
- spike_count (avg): `0`
- synops (avg): `0`
- latency_proxy_ms: `4.77`
- wall_ms: `0.229`
- budget_ok: **True**

## Raw metrics

```json
{
  "accuracy": 0.8636,
  "brain_role": "explain_plan",
  "bridge_version": "0.3.0",
  "budget_ok": true,
  "class_fix": "specialist",
  "domain": "synapse_import",
  "escalate_rate": 0.0682,
  "f1": 0.8636,
  "import_source": "/Users/valentin/Projects/neurolab/sandbox/examples/synapse_e5_import/fixtures/e5-official.json",
  "latency_proxy_ms": 4.77,
  "metric_primary": "accuracy",
  "n_neurons": 0,
  "n_synapses": 0,
  "notes": "Roles v0.3: class_fix=specialist (+0.75 pp vs stub); Outpost=explain/plan only. spike/synops N/A host wrap. oracle_accuracy lab upper bound.",
  "oracle_accuracy": 0.8902,
  "project_id": "synapse-e5-import",
  "rescue_accuracy": 0.8674,
  "seed": 0,
  "specialist_accuracy": 0.8636,
  "spike_count": 0,
  "stage_vote_accuracy": 0.8598,
  "stub_accuracy": 0.8561,
  "synapse_pack": "e5-brain-escalate",
  "synops": 0,
  "wall_ms": 0.229
}
```
