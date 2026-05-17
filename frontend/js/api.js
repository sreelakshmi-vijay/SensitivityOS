const API_BASE_URL = "http://127.0.0.1:8000";

async function fetchClassificationResults() {

    const response = await fetch(
        `${API_BASE_URL}/classify`
    );

    return await response.json();
}

async function fetchGraph() {

    const response = await fetch(
        `${API_BASE_URL}/graph`
    );

    return await response.json();
}