/**
 * API client module for Air Pollution Prediction backend.
 * Uses relative endpoints to work in any deployment or development port.
 */

const API_BASE = window.location.origin;

const apiClient = {
    async checkHealth() {
        try {
            const res = await fetch(`${API_BASE}/health`, {
                method: "GET",
                headers: { "Accept": "application/json" }
            });
            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                return { ok: false, status: res.status, data: errData };
            }
            const data = await res.json();
            return { ok: true, status: res.status, data };
        } catch (err) {
            return { ok: false, error: err.message };
        }
    },

    async predict(formData) {
        try {
            const res = await fetch(`${API_BASE}/predict`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify(formData)
            });

            const data = await res.json().catch(() => ({}));
            if (!res.ok) {
                return {
                    ok: false,
                    status: res.status,
                    error: data.detail || (Array.isArray(data.detail) ? data.detail[0]?.msg : "Prediction failed")
                };
            }
            return { ok: true, status: res.status, data };
        } catch (err) {
            return { ok: false, error: err.message };
        }
    },

    async getModelInfo() {
        try {
            const res = await fetch(`${API_BASE}/model-info`);
            if (!res.ok) return null;
            return await res.json();
        } catch (err) {
            console.error("Failed to fetch model info:", err);
            return null;
        }
    },

    async getHistoricalStats() {
        try {
            const res = await fetch(`${API_BASE}/historical-stats`);
            if (!res.ok) return null;
            return await res.json();
        } catch (err) {
            console.error("Failed to fetch historical stats:", err);
            return null;
        }
    },

    async getSampleRecords() {
        try {
            const res = await fetch(`${API_BASE}/sample-records`);
            if (!res.ok) return [];
            return await res.json();
        } catch (err) {
            console.error("Failed to fetch sample records:", err);
            return [];
        }
    }
};

window.apiClient = apiClient;
