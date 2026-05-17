async function loadDashboard() {

    const data = await fetchClassificationResults();

    renderEntities(data.columns_detected);
    renderLLMAnalysis(data.llm_analysis);
    renderReviewQueue(data.review_queue);
}

function renderEntities(entities) {

    const container = document.getElementById("entities");

    container.innerHTML = "";

    entities.forEach(entity => {

        const div = document.createElement("div");

        div.className = "entity-item";

        div.innerHTML = `
            <strong>${entity}</strong>
        `;

        container.appendChild(div);
    });
}

function renderLLMAnalysis(analysis) {

    const container = document.getElementById(
        "llm-analysis"
    );

    container.innerHTML = "";

    Object.entries(analysis).forEach(([column, result]) => {

        const div = document.createElement("div");

        div.className = "analysis-item";

        div.innerHTML = `
            <p><strong>Column:</strong> ${column}</p>
            <p>
                <strong>Sensitivity:</strong>
                <span class="${result.sensitivity}">
                    ${result.sensitivity}
                </span>
            </p>
            <p>
                <strong>Confidence:</strong>
                ${result.confidence}
            </p>
            <p>
                <strong>Reasoning:</strong>
                ${result.reasoning}
            </p>
        `;

        container.appendChild(div);
    });
}

function renderReviewQueue(reviewQueue) {

    const container = document.getElementById(
        "review-queue"
    );

    container.innerHTML = "";

    Object.entries(reviewQueue).forEach(([column, result]) => {

        const div = document.createElement("div");

        div.className = "review-item";

        div.innerHTML = `
            <p><strong>${column}</strong></p>
            <p>Confidence: ${result.confidence}</p>
            <p>${result.reasoning}</p>
        `;

        container.appendChild(div);
    });
}

loadDashboard();