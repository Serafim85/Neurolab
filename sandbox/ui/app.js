/* CS-P03 Port — wire Run / Results / Export to /api/* */
(() => {
  const $ = (id) => document.getElementById(id);
  const METRIC_ORDER = [
    "f1",
    "accuracy",
    "spike_count",
    "synops",
    "latency_proxy_ms",
    "wall_ms",
    "chip_fit_score",
    "fit_score",
    "unit_cost_eur",
  ];
  const METRIC_SKIP = new Set([
    "project_id",
    "domain",
    "seed",
    "by_scenario",
    "by_scenario_mode",
    "metric_primary",
    "economy_cost_key",
    "economy_cost_unit",
    "n_test",
    "estimate_disclaimer",
    "quality_per_kspike",
    "quality_per_ksynop",
    "quality_per_unit_cost",
  ]);

  const els = {
    project: $("project"),
    seed: $("seed"),
    scenarios: $("scenarios"),
    run: $("run"),
    cancel: $("cancel"),
    progress: $("progress"),
    progLabel: $("prog-label"),
    metrics: $("metrics"),
    scenarioHead: $("scenario-head"),
    scenarioBody: $("scenario-body"),
    metaPath: $("meta-path"),
    dlMetrics: $("dl-metrics"),
    dlReport: $("dl-report"),
  };

  function metricKeys(m) {
    if (!m) return ["budget_ok"];
    const present = new Set();
    const primary = m.metric_primary;
    if (typeof primary === "string" && m[primary] != null) present.add(primary);
    for (const k of METRIC_ORDER) {
      if (m[k] != null) present.add(k);
    }
    for (const [k, v] of Object.entries(m)) {
      if (METRIC_SKIP.has(k)) continue;
      if (typeof v === "number" || typeof v === "boolean") present.add(k);
    }
    const keys = [];
    const seen = new Set(["budget_ok"]);
    if (primary && present.has(primary)) {
      keys.push(primary);
      seen.add(primary);
    }
    for (const k of METRIC_ORDER) {
      if (present.has(k) && !seen.has(k)) {
        keys.push(k);
        seen.add(k);
      }
    }
    for (const k of [...present].sort()) {
      if (!seen.has(k)) keys.push(k);
    }
    if (m.budget_ok != null && !keys.includes("budget_ok")) keys.push("budget_ok");
    return keys;
  }

  function scenarioColumns(by, metrics) {
    const rows = by && typeof by === "object" ? Object.values(by) : [];
    const present = new Set(["n"]);
    for (const row of rows) {
      if (!row || typeof row !== "object") continue;
      for (const [k, v] of Object.entries(row)) {
        if (k !== "n" && (typeof v === "number" || typeof v === "boolean")) {
          present.add(k);
        }
      }
    }
    if (!present.size && metrics) {
      for (const k of metricKeys(metrics)) present.add(k);
    }
    const primary = metrics?.metric_primary;
    const cols = ["n"];
    const seen = new Set(["n", "budget_ok"]);
    if (typeof primary === "string" && present.has(primary)) {
      cols.push(primary);
      seen.add(primary);
    }
    for (const k of METRIC_ORDER) {
      if (present.has(k) && !seen.has(k)) {
        cols.push(k);
        seen.add(k);
      }
    }
    for (const k of [...present].sort()) {
      if (!seen.has(k)) cols.push(k);
    }
    if (present.has("budget_ok") && !cols.includes("budget_ok")) cols.push("budget_ok");
    return cols;
  }

  function setProgress(state, text) {
    els.progress.className = "progress " + state;
    els.progLabel.className =
      "prog-label" + (state === "done" ? " ok" : state === "fail" ? " err" : "");
    els.progLabel.textContent = text;
  }

  function fmt(v) {
    if (typeof v === "boolean") return v ? "true" : "false";
    if (typeof v === "number") {
      return Number.isInteger(v) ? String(v) : v.toFixed(4).replace(/\.?0+$/, (m) =>
        m.includes(".") ? m.replace(/0+$/, "").replace(/\.$/, "") : m
      );
    }
    return v == null ? "—" : String(v);
  }

  function renderMetrics(m) {
    const keys = metricKeys(m);
    els.metrics.innerHTML = "";
    for (const k of keys) {
      const card = document.createElement("div");
      card.className = "metric";
      const val = m ? m[k] : null;
      let cls = "v";
      if (k === "budget_ok") cls += val ? " ok" : " bad";
      card.innerHTML =
        `<div class="k">${k}</div><div class="${cls}">${fmt(val)}</div>`;
      els.metrics.appendChild(card);
    }
  }

  function renderScenarios(names, metrics) {
    const by = (metrics && metrics.by_scenario) || {};
    const cols = scenarioColumns(by, metrics);
    if (els.scenarioHead) {
      els.scenarioHead.innerHTML =
        "<tr><th>Scenario</th>" + cols.map((c) => `<th>${c}</th>`).join("") + "</tr>";
    }
    els.scenarioBody.innerHTML = "";
    const keys = names && names.length ? names : Object.keys(by);
    if (!keys.length) {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td colspan="${cols.length + 1}"><code>—</code> no scenarios in manifest</td>`;
      els.scenarioBody.appendChild(tr);
      return;
    }
    for (const name of keys) {
      const row = by[name];
      const tr = document.createElement("tr");
      const cells = cols.map((c) => `<td>${fmt(row ? row[c] : metrics?.[c])}</td>`).join("");
      tr.innerHTML = `<td><code>${name}</code></td>${cells}`;
      els.scenarioBody.appendChild(tr);
    }
  }

  async function loadProject() {
    const path = els.project.value.trim();
    const q = path ? `?path=${encodeURIComponent(path)}` : "";
    const res = await fetch("/api/project" + q);
    const data = await res.json();
    if (!data.ok && data.error) throw new Error(data.error);
    if (data.project?.path) els.project.value = data.project.path;
    if (data.default_seed != null) els.seed.value = String(data.default_seed);
    els.metaPath.textContent = `project: ${data.project?.id || "?"} · ${data.project?.domain || ""}`;
    const names = data.scenarios || [];
    els.scenarios.innerHTML = "";
    const all = document.createElement("option");
    all.value = "__all__";
    all.textContent = names.length ? names.join(" · ") : "(manifest scenarios)";
    els.scenarios.appendChild(all);
    for (const n of names) {
      const o = document.createElement("option");
      o.value = n;
      o.textContent = n;
      els.scenarios.appendChild(o);
    }
    if (data.last_metrics) {
      renderMetrics(data.last_metrics);
      renderScenarios(names, data.last_metrics);
      setProgress(
        "done",
        `loaded last out/metrics.json · budget_ok=${data.last_metrics.budget_ok}`
      );
    } else {
      renderScenarios(names, null);
      setProgress("", "idle · press Run");
    }
  }

  function clearMetricsPending() {
    els.metrics.innerHTML = "";
    const card = document.createElement("div");
    card.className = "metric";
    card.innerHTML = `<div class="k">…</div><div class="v muted">running</div>`;
    els.metrics.appendChild(card);
  }

  function paintFrame() {
    return new Promise((resolve) => {
      requestAnimationFrame(() => requestAnimationFrame(resolve));
    });
  }

  async function run() {
    els.run.disabled = true;
    els.cancel.disabled = true;
    clearMetricsPending();
    setProgress("running", "running · closed-sandbox run …");
    await paintFrame();
    const t0 = performance.now();
    try {
      const body = {
        project: els.project.value.trim() || null,
        seed: Number(els.seed.value),
      };
      const res = await fetch("/api/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (!res.ok || data.ok === false) {
        throw new Error(data.error || `HTTP ${res.status}`);
      }
      const wallUi = Math.round(performance.now() - t0);
      renderMetrics(data.metrics);
      renderScenarios(data.scenarios, data.metrics);
      els.metaPath.textContent =
        `project: ${data.project.id} · ${data.project.domain} · out: ${data.out_dir}`;
      setProgress(
        "done",
        `done · budget_ok=${data.metrics.budget_ok} · engine ${fmt(data.metrics.wall_ms)} ms · ui ${wallUi} ms · ${new Date().toLocaleTimeString()}`
      );
    } catch (err) {
      setProgress("fail", `error · ${err.message || err}`);
    } finally {
      els.run.disabled = false;
    }
  }

  els.run.addEventListener("click", () => {
    run();
  });
  els.dlMetrics.addEventListener("click", () => {
    window.location.href = "/api/export/metrics.json";
  });
  els.dlReport.addEventListener("click", () => {
    window.location.href = "/api/export/report.md";
  });
  els.project.addEventListener("change", () => {
    loadProject().catch((e) => setProgress("fail", String(e.message || e)));
  });

  const qs = new URL(window.location.href).searchParams.get("project");
  if (qs) els.project.value = qs;

  loadProject().catch((e) => setProgress("fail", String(e.message || e)));
})();
