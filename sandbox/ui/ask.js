/* CS-P05 Port — Ask ↔ /api/ask (CLI parity + contour honesty) */
(() => {
  const $ = (id) => document.getElementById(id);
  const els = {
    project: $("project"),
    metrics: $("metrics"),
    provider: $("provider"),
    bannerLocal: $("banner-local"),
    bannerPublic: $("banner-public"),
    attach: $("attach"),
    thread: $("thread-msgs"),
    question: $("question"),
    ask: $("ask"),
    meta: $("meta-status"),
  };

  function syncBanner() {
    const pub = els.provider.value === "public";
    // FR-UI-031: public banner cannot be hidden when provider=public
    els.bannerPublic.hidden = !pub;
    els.bannerLocal.hidden = pub;
  }

  function addMsg(who, text, cls) {
    const div = document.createElement("div");
    div.className = "msg" + (cls ? " " + cls : "");
    div.innerHTML =
      `<div class="who">${who}</div><p></p>`;
    div.querySelector("p").textContent = text;
    els.thread.appendChild(div);
    els.thread.parentElement.scrollTop = els.thread.parentElement.scrollHeight;
  }

  async function loadContour() {
    const path = els.project.value.trim();
    const q = path ? `?path=${encodeURIComponent(path)}` : "";
    const res = await fetch("/api/project" + q);
    const data = await res.json();
    if (!data.ok) throw new Error(data.error || "project load failed");
    const c = data.contour || {};
    if (c.provider === "public" || c.provider === "local") {
      els.provider.value = c.provider;
    }
    const metricsHint =
      els.metrics.value.trim() ||
      (data.out_dir ? data.out_dir.replace(/.*\/sandbox\//, "") + "/metrics.json" : "out/metrics.json");
    els.attach.textContent =
      `attached · ${metricsHint} · project ${data.project?.id || "?"} · domain ${data.project?.domain || "?"}` +
      (c.model ? ` · model ${c.model}` : "");
    syncBanner();
    els.meta.textContent = `provider=${els.provider.value}`;
    return data;
  }

  async function runAsk() {
    const question = els.question.value.trim();
    if (!question) {
      els.meta.textContent = "empty question";
      return;
    }
    els.ask.disabled = true;
    addMsg("engineer", question, "user");
    els.meta.textContent = "asking …";
    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project: els.project.value.trim() || null,
          metrics: els.metrics.value.trim() || null,
          question,
          provider: els.provider.value,
        }),
      });
      const data = await res.json();
      if (!res.ok || data.ok === false) {
        throw new Error(data.error || `HTTP ${res.status}`);
      }
      const who = `ask · ${data.provider} · ${data.model || "?"}`;
      addMsg(who, data.answer || "(empty)");
      if (data.warning) {
        // keep banner; also stamp thread
        addMsg("contour", data.warning, "warn");
      }
      if (data.attached) {
        els.attach.textContent =
          `attached · ${data.attached.metrics || "metrics"} · ${data.attached.project || "project"}`;
      }
      els.meta.textContent = `ok · ${data.provider}`;
    } catch (err) {
      addMsg("error", String(err.message || err), "err");
      els.meta.textContent = "error";
    } finally {
      els.ask.disabled = false;
    }
  }

  els.provider.addEventListener("change", () => {
    syncBanner();
    els.meta.textContent = `provider=${els.provider.value}`;
  });
  els.ask.addEventListener("click", () => {
    runAsk();
  });
  els.question.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter") {
      ev.preventDefault();
      runAsk();
    }
  });
  els.project.addEventListener("change", () => {
    loadContour().catch((e) => {
      els.meta.textContent = String(e.message || e);
    });
  });

  syncBanner();
  loadContour().catch(() => {
    syncBanner();
  });
})();
