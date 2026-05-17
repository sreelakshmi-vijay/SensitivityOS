async function loadDashboard() {

    const data = await fetchClassificationResults();

    renderEntities(data.columns_detected);

    renderLLMAnalysis(data.llm_analysis);

    renderReviewQueue(data.review_queue);

    await renderGraph();

    setupReviewForm();
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

            <p>
                Confidence:
                ${result.confidence}
            </p>

            <p>
                ${result.reasoning}
            </p>

            <button
                onclick="populateReviewForm(
                    '${column}',
                    '${result.sensitivity}'
                )">
                Review
            </button>
        `;

        container.appendChild(div);
    });
}

async function renderGraph() {

    const graphData = await fetchGraph();

    const container = document.getElementById("graph");

    const nodes = new vis.DataSet(

        graphData.nodes.map(node => ({

            id: node.id,

            label: node.label,

            color: getSensitivityColor(
                node.sensitivity
            ),

            shape: "dot",

            size: 20
        }))
    );

    const edges = new vis.DataSet(

        graphData.edges.map(edge => ({

            from: edge.from,

            to: edge.to,

            label: edge.label,

            arrows: "to",

            width: edge.weight * 5
        }))
    );

    const data = {
        nodes,
        edges
    };

    const options = {

        physics: {
            enabled: true
        },

        edges: {
            smooth: true,
            font: {
                size: 12
            }
        },

        nodes: {
            font: {
                color: "#fff"
            }
        }
    };

    new vis.Network(
        container,
        data,
        options
    );
}

function getSensitivityColor(sensitivity) {

    switch (sensitivity) {

        case "critical":
            return "#7c3aed";

        case "high":
            return "#dc2626";

        case "medium":
            return "#d97706";

        case "low":
            return "#16a34a";

        default:
            return "#6b7280";
    }
}

function populateReviewForm(
    entity,
    originalSensitivity
) {

    document.getElementById(
        "review-entity"
    ).value = entity;

    document.getElementById(
        "review-original"
    ).value = originalSensitivity;

    document.getElementById(
        "review-relationship"
    ).value = "strongly_escalates";
}

function setupReviewForm() {

    const button = document.getElementById(
        "submit-review"
    );

    button.addEventListener("click", async () => {

        const payload = {

            entity: document.getElementById(
                "review-entity"
            ).value,

            original_sensitivity: document.getElementById(
                "review-original"
            ).value,

            corrected_sensitivity: document.getElementById(
                "review-corrected"
            ).value,

            relationship: document.getElementById(
                "review-relationship"
            ).value,

            confidence_adjustment: parseFloat(

                document.getElementById(
                    "review-adjustment"
                ).value
            )
        };

        const response = await submitReviewDecision(
            payload
        );

        document.getElementById(
            "review-response"
        ).innerHTML = `
            ${response.message}
        `;
    });
}

loadDashboard();