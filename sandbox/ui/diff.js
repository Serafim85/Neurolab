/* CS-P04 Port — Diff ↔ /api/diff (CLI parity) */
(() => {
  const $ = (id) => document.getElementById(id);
  const els = {
    a: $("path-a"),
    b: $("path-b"),
    btn: $("diff"),
    summary: $("summary"),
    body: $("diff-body"),
    meta: $("meta-status"),
  };

  const DEFAULT_A = "examples/anomaly_v0/out/seed42/metrics.json";
  const DEFAULT_B = "examples/anomaly_v0/out/seed43/metrics.json";

  function fmt(v) {
    if (typeof v === "boolean") return v ? "true" : "false";
    if (typeof v === "number") {
      if (Number.isInteger(v)) return String(v);
      return v.toFixed(4).replace(/\.?0+$/, (m) =>
        m.includes(".") ? m.replace(/0+$/, "").replace(/\.$/, "") : m
      );
    }
    if (v == null) return "—";
    if (typeof v === "object") return "{…}";
    return String(v);
  }

  function deltaClass(delta) {
    if (typeof delta !== "number") return "same";
    if (delta > 0) return "up";
    if (delta < 0) return "down";
    return "same";
  }

  function fmtDelta(entry) {
    if (typeof entry.delta === "number") {
      const d = entry.delta;
      const sign = d > 0 ? "+" : "";
      return sign + fmt(d);
    }
    return "—";
  }

  function isScalarRow(entry) {
    const a = entry.a;
    const b = entry.b;
    const aOk =
      a == null ||
      typeof a === "number" ||
      typeof a === "boolean" ||
      typeof a === "string";
    const bOk =
      b == null ||
      typeof b === "number" ||
      typeof b === "boolean" ||
      typeof b === "string";
    return aOk && bOk;
  }

  function shortPath(p) {
    if (!p) return "?";
    const marker = "/sandbox/";
    const i = p.indexOf(marker);
    return i >= 0 ? p.slice(i + marker.length) : p;
  }

  function render(payload) {
    const result = payload.diff || payload;
    const changed = result.changed || {};
    const keys = Object.keys(changed).sort();
    const scalarKeys = keys.filter((k) => isScalarRow(changed[k]));
    els.body.innerHTML = "";
    if (!scalarKeys.length) {
      const tr = document.createElement("tr");
      const sameFile =
        payload.a && payload.b && payload.a === payload.b
          ? " · A and B resolve to the same path"
          : "";
      tr.innerHTML =
        `<td colspan="4"><code>—</code> no scalar changes` +
        (result.n_changed
          ? ` (n_changed=${result.n_changed} incl. nested)`
          : " · files identical on scalar keys") +
        `${sameFile}</td>`;
      els.body.appendChild(tr);
    } else {
      for (const key of scalarKeys) {
        const entry = changed[key];
        const tr = document.createElement("tr");
        const cls = deltaClass(entry.delta);
        tr.innerHTML = `
          <td>${key}</td>
          <td>${fmt(entry.a)}</td>
          <td>${fmt(entry.b)}</td>
          <td class="delta ${cls}">${fmtDelta(entry)}</td>`;
        els.body.appendChild(tr);
      }
    }
    const nested = (result.n_changed || 0) - scalarKeys.length;
    const paths =
      payload.a && payload.b
        ? `<br/><span class="paths">A: ${shortPath(payload.a)}<br/>B: ${shortPath(payload.b)}</span>`
        : "";
    els.summary.innerHTML =
      `<strong>n_changed</strong> = ${result.n_changed}` +
      (nested > 0
        ? ` · table ${scalarKeys.length} scalars (${nested} nested skipped)`
        : "") +
      paths;
    els.summary.className =
      "summary" + (result.n_changed ? " ok" : "");
    els.meta.textContent = `n_changed=${result.n_changed}`;
  }

  async function runDiff() {
    const pathA = els.a.value.trim();
    const pathB = els.b.value.trim();
    if (!pathA || !pathB) {
      els.summary.textContent = "error · set both A and B paths";
      els.summary.className = "summary err";
      return;
    }
    if (pathA === pathB) {
      els.summary.innerHTML =
        "A and B are the <strong>same path</strong> — n_changed will be 0. Pick two runs (e.g. seed42 vs seed43).";
      els.summary.className = "summary err";
      els.meta.textContent = "same path";
      els.body.innerHTML =
        `<tr><td colspan="4"><code>—</code> identical path</td></tr>`;
      return;
    }
    els.btn.disabled = true;
    els.summary.textContent = "diffing …";
    els.summary.className = "summary";
    try {
      const res = await fetch("/api/diff", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ a: pathA, b: pathB }),
      });
      const data = await res.json();
      if (!res.ok || data.ok === false) {
        throw new Error(data.error || `HTTP ${res.status}`);
      }
      render(data);
    } catch (err) {
      els.summary.textContent = `error · ${err.message || err}`;
      els.summary.className = "summary err";
      els.meta.textContent = "error";
      els.body.innerHTML =
        `<tr><td colspan="4"><code>—</code></td></tr>`;
    } finally {
      els.btn.disabled = false;
    }
  }

  els.btn.addEventListener("click", () => {
    runDiff();
  });
  for (const input of [els.a, els.b]) {
    input.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter") {
        ev.preventDefault();
        runDiff();
      }
    });
  }

  if (!els.a.value) els.a.value = DEFAULT_A;
  if (!els.b.value) els.b.value = DEFAULT_B;
  runDiff();
})();
