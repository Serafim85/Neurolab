/* CS-P02 Port — Editor ↔ /api/manifest + /api/validate */
(() => {
  const $ = (id) => document.getElementById(id);
  const els = {
    path: $("path"),
    toml: $("toml"),
    load: $("load"),
    validate: $("validate"),
    save: $("save"),
    run: $("run"),
    domain: $("badge-domain"),
    pid: $("badge-id"),
    msg: $("msg"),
    okmsg: $("okmsg"),
    meta: $("meta-status"),
    preview: $("form-preview"),
    tabForm: $("tab-form"),
    tabRaw: $("tab-raw"),
    paneForm: $("pane-form"),
    paneRaw: $("pane-raw"),
    fHidden: $("f-n-hidden"),
    fSpikes: $("f-max-spikes"),
    fSeed: $("f-seed"),
    fProvider: $("f-provider"),
    fMetric: $("f-metric"),
    applyForm: $("apply-form"),
  };

  let valid = false;

  function qsProject() {
    const u = new URL(window.location.href);
    return u.searchParams.get("project");
  }

  function setValid(ok, err) {
    valid = !!ok;
    els.run.disabled = !valid;
    els.okmsg.hidden = !valid;
    if (ok) {
      els.msg.hidden = true;
      els.msg.textContent = "";
    } else if (err) {
      els.msg.hidden = false;
      els.msg.innerHTML = `<strong>VALIDATION</strong><div style="margin-top:4px"></div>`;
      els.msg.querySelector("div").textContent = err;
    }
    els.meta.textContent = ok ? "valid" : err ? "invalid" : "idle";
  }

  function fillForm(form) {
    if (!form) return;
    if (form.n_hidden != null) els.fHidden.value = form.n_hidden;
    if (form.max_spikes_per_sample != null) els.fSpikes.value = form.max_spikes_per_sample;
    if (form.seed != null) els.fSeed.value = form.seed;
    if (form.provider) els.fProvider.value = form.provider;
    if (form.metric_primary != null) els.fMetric.value = form.metric_primary;
    els.preview.textContent = JSON.stringify(form, null, 2);
  }

  function patchTomlKey(text, table, key, value) {
    const lines = text.split("\n");
    let inTable = table === "" || table === "root";
    const want = table ? `[${table}]` : null;
    let replaced = false;
    const out = [];
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const t = line.trim();
      if (t.startsWith("[") && t.endsWith("]")) {
        inTable = want ? t === want || t.startsWith(`[${table}.`) : false;
        if (want && t === want) inTable = true;
        if (want && t !== want && !t.startsWith(`[${table}.`)) {
          if (t.startsWith("[") && table) inTable = t === `[${table}]`;
        }
        // simpler: exact table header match
        inTable = want ? t === `[${table}]` : false;
      }
      if (inTable && new RegExp(`^\\s*${key}\\s*=`).test(line)) {
        const q = typeof value === "string" ? `"${value}"` : String(value);
        out.push(`${key} = ${q}`);
        replaced = true;
        continue;
      }
      out.push(line);
    }
    if (!replaced && table && value != null && value !== "") {
      // append under table if missing
      const header = `[${table}]`;
      const idx = out.findIndex((l) => l.trim() === header);
      const q = typeof value === "string" ? `"${value}"` : String(value);
      if (idx >= 0) out.splice(idx + 1, 0, `${key} = ${q}`);
    }
    return out.join("\n");
  }

  function applyFormToRaw() {
    let text = els.toml.value;
    const nHidden = els.fHidden.value;
    const spikes = els.fSpikes.value;
    const seed = els.fSeed.value;
    const provider = els.fProvider.value;
    const metric = els.fMetric.value;
    if (nHidden !== "") text = patchTomlKey(text, "network", "n_hidden", Number(nHidden));
    if (spikes !== "")
      text = patchTomlKey(text, "budget", "max_spikes_per_sample", Number(spikes));
    if (seed !== "") text = patchTomlKey(text, "sandbox", "seed", Number(seed));
    if (provider) text = patchTomlKey(text, "contour", "provider", provider);
    if (metric) text = patchTomlKey(text, "task", "metric_primary", metric);
    els.toml.value = text;
    setValid(false, null);
    els.meta.textContent = "form applied — validate again";
  }

  async function loadManifest() {
    const path = els.path.value.trim();
    els.meta.textContent = "loading…";
    const res = await fetch("/api/manifest?path=" + encodeURIComponent(path));
    const data = await res.json();
    if (!res.ok || data.ok === false) throw new Error(data.error || "load failed");
    els.toml.value = data.toml || "";
    els.domain.textContent = `domain · ${data.project?.domain || "—"}`;
    els.pid.textContent = `project · ${data.project?.id || "—"}`;
    fillForm(data.form);
    setValid(!!data.valid, data.error || null);
  }

  async function validate() {
    els.meta.textContent = "validating…";
    const res = await fetch("/api/validate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        project: els.path.value.trim(),
        toml: els.toml.value,
      }),
    });
    const data = await res.json();
    if (data.project?.domain)
      els.domain.textContent = `domain · ${data.project.domain}`;
    if (data.project?.id) els.pid.textContent = `project · ${data.project.id}`;
    fillForm(data.form);
    setValid(!!data.valid, data.error || (!data.valid ? "invalid" : null));
  }

  async function save() {
    await validate();
    if (!valid) return;
    const res = await fetch("/api/manifest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        project: els.path.value.trim(),
        toml: els.toml.value,
      }),
    });
    const data = await res.json();
    if (!res.ok || data.ok === false) {
      setValid(false, data.error || "save failed");
      return;
    }
    els.meta.textContent = "saved";
  }

  function showTab(which) {
    const form = which === "form";
    els.tabForm.classList.toggle("on", form);
    els.tabRaw.classList.toggle("on", !form);
    els.paneForm.hidden = !form;
    els.paneRaw.hidden = form;
  }

  els.load.addEventListener("click", () => {
    loadManifest().catch((e) => setValid(false, String(e.message || e)));
  });
  els.validate.addEventListener("click", () => {
    validate().catch((e) => setValid(false, String(e.message || e)));
  });
  els.save.addEventListener("click", () => {
    save().catch((e) => setValid(false, String(e.message || e)));
  });
  els.run.addEventListener("click", () => {
    if (!valid) return;
    const p = els.path.value.trim();
    window.location.href = "/run?project=" + encodeURIComponent(p);
  });
  els.applyForm.addEventListener("click", () => applyFormToRaw());
  els.tabForm.addEventListener("click", () => showTab("form"));
  els.tabRaw.addEventListener("click", () => showTab("raw"));
  els.toml.addEventListener("input", () => setValid(false, null));

  const fromQs = qsProject();
  if (fromQs) els.path.value = fromQs;
  showTab("raw");
  loadManifest().catch((e) => setValid(false, String(e.message || e)));
})();
