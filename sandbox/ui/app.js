/* CS-P03 Port — wire Run / Results / Export to /api/* */
(() => {
  const $ = (id) => document.getElementById(id);
  const METRIC_KEYS = [
    "f1",
    "accuracy",
    "spike_count",
    "synops",
    "latency_proxy_ms",
    "budget_ok",
  ];

  const els = {
    project: $("project"),
    seed: $("seed"),
    scenarios: $("scenarios"),
    run: $("run"),
    cancel: $("cancel"),
    progress: $("progress"),
    progLabel: $("prog-label"),
    metrics: $("metrics"),
    scenarioBody: $("scenario-body"),
    metaPath: $("meta-path"),
    dlMetrics: $("dl-metrics"),
    dlReport: $("dl-report"),
  };

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
    els.metrics.innerHTML = "";
    for (const k of METRIC_KEYS) {
      const card = document.createElement("div");
      card.className = "metric";
      const val = m[k];
      let cls = "v";
      if (k === "budget_ok") cls += val ? " ok" : " bad";
      card.innerHTML =
        `<div class="k">${k}</div><div class="${cls}">${fmt(val)}</div>`;
      els.metrics.appendChild(card);
    }
  }

  function renderScenarios(names, metrics) {
    els.scenarioBody.innerHTML = "";
    const by = (metrics && metrics.by_scenario) || {};
    const keys = names && names.length ? names : Object.keys(by);
    if (!keys.length) {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td colspan="6"><code>—</code> no scenarios in manifest</td>`;
      els.scenarioBody.appendChild(tr);
      return;
    }
    for (const name of keys) {
      const row = by[name];
      const tr = document.createElement("tr");
      if (row) {
        tr.innerHTML = `
          <td><code>${name}</code></td>
          <td>${fmt(row.n)}</td>
          <td>${fmt(row.f1)}</td>
          <td>${fmt(row.accuracy)}</td>
          <td>${fmt(row.spike_count)}</td>
          <td>${fmt(row.synops)}</td>`;
      } else {
        // Fallback if by_scenario missing — show aggregate once-labeled.
        tr.innerHTML = `
          <td><code>${name}</code></td>
          <td>—</td>
          <td>${fmt(metrics?.f1)}</td>
          <td>${fmt(metrics?.accuracy)}</td>
          <td>${fmt(metrics?.spike_count)}</td>
          <td>${fmt(metrics?.synops)}</td>`;
      }
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
    for (const k of METRIC_KEYS) {
      const card = document.createElement("div");
      card.className = "metric";
      card.innerHTML = `<div class="k">${k}</div><div class="v muted">…</div>`;
      els.metrics.appendChild(card);
    }
  }

  function paintFrame() {
    // Ensure "running" UI paints before a fast /api/run returns.
    return new Promise((resolve) => {
      requestAnimationFrame(() => requestAnimationFrame(resolve));
    });
  }

  async function run() {
    els.run.disabled = true;
    els.cancel.disabled = true; // sync engine — cancel waived (parity)
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
