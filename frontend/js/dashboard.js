const SENSITIVITY_COLORS = {
    public:       "#16a34a",
    internal:     "#2563eb",
    confidential: "#d97706",
    restricted:   "#dc2626",
};

// On page load, just render the graph (no auto-classify call to broken hardcoded route)
async function loadDashboard() {
    await renderGraph();
    setupReviewForm();
    setupFileUpload();
}

// ── Final classifications (merged 3-layer result) ─────────────────────────────
function renderFinalClassifications(finalClassifications) {

    const container = document.getElementById("final-classifications");
    container.innerHTML = "";

    if (!finalClassifications || Object.keys(finalClassifications).length === 0) {
        container.innerHTML = "<p>No classifications yet. Upload a CSV to begin.</p>";
        return;
    }

    Object.entries(finalClassifications).forEach(([column, result]) => {

        const div = document.createElement("div");
        div.className = "analysis-item";

        const color = SENSITIVITY_COLORS[result.final_sensitivity] || "#6b7280";
        const sources = (result.sources_used || []).join(", ") || "none";

        div.innerHTML = `
            <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
                <strong>${column}</strong>
                <span class="badge ${result.final_sensitivity}">${result.final_sensitivity}</span>
                <span style="font-size:13px;color:#6b7280">confidence: ${(result.confidence * 100).toFixed(0)}%</span>
                ${result.needs_human_review ? '<span class="badge review-flag">⚑ needs review</span>' : ''}
            </div>
            <div style="font-size:13px;margin-top:4px;color:#555">Sources: ${sources}</div>
        `;

        container.appendChild(div);
    });
}

// ── LLM Analysis ──────────────────────────────────────────────────────────────
function renderLLMAnalysis(analysis) {

    const container = document.getElementById("llm-analysis");
    container.innerHTML = "";

    if (!analysis || Object.keys(analysis).length === 0) {
        container.innerHTML = "<p>LLM was not called (Presidio handled all columns at high confidence).</p>";
        return;
    }

    Object.entries(analysis).forEach(([column, result]) => {

        const div = document.createElement("div");
        div.className = "analysis-item";
        div.innerHTML = `
            <p><strong>Column:</strong> ${column}</p>
            <p><strong>Sensitivity:</strong> <span class="${result.sensitivity}">${result.sensitivity}</span></p>
            <p><strong>Confidence:</strong> ${(result.confidence * 100).toFixed(0)}%</p>
            <p><strong>Reasoning:</strong> ${result.reasoning}</p>
        `;

        container.appendChild(div);
    });
}

// ── Review Queue ──────────────────────────────────────────────────────────────
function renderReviewQueue(reviewQueue) {

    const container = document.getElementById("review-queue");
    container.innerHTML = "";

    if (!reviewQueue || Object.keys(reviewQueue).length === 0) {
        container.innerHTML = "<p>No items in review queue.</p>";
        return;
    }

    Object.entries(reviewQueue).forEach(([column, result]) => {

        const div = document.createElement("div");
        div.className = "review-item";
        div.innerHTML = `
            <p><strong>${column}</strong> — <span class="${result.final_sensitivity}">${result.final_sensitivity}</span></p>
            <p>Confidence: ${(result.confidence * 100).toFixed(0)}%</p>
            <button onclick="populateReviewForm('${column}', '${result.final_sensitivity}')">
                Review
            </button>
        `;

        container.appendChild(div);
    });
}

// ── Graph ─────────────────────────────────────────────────────────────────────
async function renderGraph() {

    const graphData = await fetchGraph();
    const container = document.getElementById("graph");

    const nodes = new vis.DataSet(
        graphData.nodes.map(node => ({
            id: node.id,
            label: node.id,
            color: SENSITIVITY_COLORS[node.sensitivity] || "#6b7280",
            shape: "dot",
            size: 20,
            font: { color: "#fff" },
            title: `Sensitivity: ${node.sensitivity}`,
        }))
    );

    const edges = new vis.DataSet(
        graphData.edges.map(edge => ({
            from: edge.from,
            to: edge.to,
            label: edge.label,
            arrows: "to",
            width: Math.max(1, edge.weight * 5),
            title: `Weight: ${edge.weight}`,
        }))
    );

    new vis.Network(
        container,
        { nodes, edges },
        {
            physics: { enabled: true },
            edges: { smooth: true, font: { size: 11 } },
        }
    );
}

// ── Analytics ─────────────────────────────────────────────────────────────────
function renderAnalytics(data) {

    const finalClassifications = data.final_classifications || {};
    const reviewQueue = data.review_queue || {};

    document.getElementById("total-entities").innerText =
        Object.keys(finalClassifications).length;

    const counts = { public: 0, internal: 0, confidential: 0, restricted: 0 };

    Object.values(finalClassifications).forEach(result => {
        const s = result.final_sensitivity;
        if (s in counts) counts[s]++;
    });

    document.getElementById("critical-count").innerText = counts.restricted;
    document.getElementById("review-count").innerText = Object.keys(reviewQueue).length;

    renderSensitivityChart(counts);
}

function renderSensitivityChart(data) {

    const ctx = document.getElementById("sensitivityChart");

    // Destroy previous chart if any
    if (ctx._chart) ctx._chart.destroy();

    ctx._chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: "Sensitivity Distribution",
                data: Object.values(data),
                backgroundColor: Object.keys(data).map(k => SENSITIVITY_COLORS[k] || "#6b7280"),
            }],
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
        },
    });
}

// ── Explainability ────────────────────────────────────────────────────────────
function renderExplainability(data) {

    const container = document.getElementById("explainability");
    container.innerHTML = "";

    const graphInference = data.graph_inference || {};

    if (Object.keys(graphInference).length === 0) {
        container.innerHTML = "<p>No graph inference results (no columns matched graph nodes).</p>";
        return;
    }

    Object.entries(graphInference).forEach(([entity, details]) => {

        const div = document.createElement("div");
        div.className = "explain-card";

        const reasoningHtml = (details.reasoning || []).map(r => `
            <li>
                <strong>${r.connected_entity}</strong>
                via <em>${r.relationship}</em>
                (weight: ${r.weight})
                ${r.triggered_escalation ? "— <span style='color:#dc2626'>escalated</span>" : ""}
            </li>
        `).join("");

        div.innerHTML = `
            <h3>${entity}</h3>
            <p><strong>Base:</strong> <span class="${details.base_sensitivity}">${details.base_sensitivity}</span>
               &rarr; <strong>Final:</strong> <span class="${details.final_sensitivity}">${details.final_sensitivity}</span></p>
            ${reasoningHtml ? `<ul style="font-size:13px">${reasoningHtml}</ul>` : ""}
        `;

        container.appendChild(div);
    });
}

// ── Review form ───────────────────────────────────────────────────────────────
function populateReviewForm(entity, originalSensitivity) {

    document.getElementById("review-entity").value = entity;
    document.getElementById("review-original").value = originalSensitivity;
    document.getElementById("review-corrected").value = originalSensitivity;
    document.getElementById("review-relationship").value = "strongly_escalates";

    document.getElementById("review-entity").scrollIntoView({ behavior: "smooth" });
}

function setupReviewForm() {

    document.getElementById("submit-review").addEventListener("click", async () => {

        const payload = {
            entity: document.getElementById("review-entity").value,
            original_sensitivity: document.getElementById("review-original").value,
            corrected_sensitivity: document.getElementById("review-corrected").value,
            relationship: document.getElementById("review-relationship").value,
            confidence_adjustment: parseFloat(document.getElementById("review-adjustment").value),
            reviewer_note: document.getElementById("review-note").value || null,
        };

        const response = await submitReviewDecision(payload);

        document.getElementById("review-response").innerHTML =
            `<span style="color:green">${response.message}</span>`;
    });
}

// ── File upload ───────────────────────────────────────────────────────────────
function setupFileUpload() {

    document.getElementById("upload-button").addEventListener("click", async () => {

        const input = document.getElementById("file-upload");
        const file = input.files[0];

        if (!file) {
            alert("Please select a CSV file.");
            return;
        }

        const statusEl = document.getElementById("upload-status");
        statusEl.innerText = "Uploading and analysing...";

        try {

            const response = await uploadDataset(file);
            const results = response.results;

            renderFinalClassifications(results.final_classifications);
            renderLLMAnalysis(results.llm_analysis);
            renderReviewQueue(results.review_queue);
            renderAnalytics(results);
            renderExplainability(results);

            statusEl.innerText = `Analysis complete — ${Object.keys(results.final_classifications || {}).length} columns classified.`;

        } catch (error) {
            console.error(error);
            statusEl.innerText = "Upload failed. Is the backend running?";
        }
    });
}

loadDashboard();
