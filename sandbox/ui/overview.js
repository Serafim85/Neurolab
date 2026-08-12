/* CS-P01 Port — Overview ↔ /api/projects */
(() => {
  const $ = (id) => document.getElementById(id);
  const body = $("project-body");
  const head = $("project-head");
  const meta = $("meta-status");
  const hint = $("metric-hint");

  const METRIC_CANDIDATES = [
    "f1",
    "accuracy",
    "fit_score",
    "chip_fit_score",
    "spike_count",
    "synops",
    "latency_proxy_ms",
  ];

  function fmt(v) {
    if (v == null) return "—";
    if (typeof v === "boolean") return v ? "true" : "false";
    if (typeof v === "number") {
      return Number.isInteger(v) ? String(v) : v.toFixed(4).replace(/\.?0+$/, "");
    }
    return String(v);
  }

  function metricColumns(rows) {
    const cols = [];
    for (const key of METRIC_CANDIDATES) {
      if (rows.some((row) => row[key] != null)) cols.push(key);
    }
    return cols;
  }

  function statusCell(row) {
    const s = row.status;
    if (s === "ok") return '<span class="status ok">OK</span>';
    if (s === "budget") return '<span class="status fail">BUDGET</span>';
    if (s === "invalid") return '<span class="status fail">INVALID</span>';
    return '<span class="status idle">NO RUN</span>';
  }

  function render(rows) {
    const metricCols = metricColumns(rows);
    if (head) {
      head.innerHTML =
        "<tr><th>Project</th><th>Domain</th><th>Last run</th>" +
        metricCols.map((k) => `<th>${k}</th>`).join("") +
        "<th>budget_ok</th><th>Status</th><th></th></tr>";
    }
    body.innerHTML = "";
    if (!rows.length) {
      body.innerHTML = `<tr><td colspan="${5 + metricCols.length}"><code>—</code> no examples/</td></tr>`;
      return;
    }
    for (const row of rows) {
      const tr = document.createElement("tr");
      const rel = row.rel || "";
      const metricCells = metricCols.map((k) => `<td>${fmt(row[k])}</td>`).join("");
      tr.innerHTML = `
        <td><code>${row.id}</code></td>
        <td><code>${row.domain}</code></td>
        <td>${row.last_run || "—"}</td>
        ${metricCells}
        <td>${fmt(row.budget_ok)}</td>
        <td>${statusCell(row)}</td>
        <td class="actions">
          <a class="btn" href="/run?project=${encodeURIComponent(rel)}">Run</a>
          <a class="btn" href="/editor?project=${encodeURIComponent(rel)}">Edit</a>
        </td>`;
      body.appendChild(tr);
    }
    if (hint) {
      const shown = metricCols.length ? metricCols.join(" · ") : "(no metrics yet)";
      hint.textContent = `Metric columns from last run: ${shown} · budget_ok`;
    }
  }

  async function load() {
    meta.textContent = "loading…";
    try {
      const res = await fetch("/api/projects");
      const data = await res.json();
      if (!data.ok) throw new Error(data.error || "failed");
      render(data.projects || []);
      meta.textContent = `n=${data.n}`;
    } catch (err) {
      meta.textContent = String(err.message || err);
      body.innerHTML = `<tr><td colspan="8" class="status fail">${err.message || err}</td></tr>`;
    }
  }

  $("refresh").addEventListener("click", () => load());
  $("open-default").addEventListener("click", () => {
    window.location.href = "/run?project=" + encodeURIComponent("examples/anomaly_v0/project.toml");
  });
  load();
})();
