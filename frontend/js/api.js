const API_BASE_URL = "";

async function fetchGraph() {
    const response = await fetch(`${API_BASE_URL}/graph`);
    if (!response.ok) throw new Error(`Graph fetch failed: ${response.status}`);
    return await response.json();
}

async function submitReviewDecision(payload) {
    const response = await fetch(`${API_BASE_URL}/review/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error(`Review submit failed: ${response.status}`);
    return await response.json();
}

async function uploadDataset(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/upload`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        const err = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(`Upload failed (${response.status}): ${err.detail || JSON.stringify(err)}`);
    }

    return await response.json();
}