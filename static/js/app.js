/**
 * Main application coordinator for Air Pollution Prediction System.
 * Connects UI inputs, validation, API requests, health checking, and result display.
 */

document.addEventListener("DOMContentLoaded", async () => {
    // 1. Initialize core managers
    themeManager.init();
    i18n.init();
    analyticsCharts.init();

    // 2. Bind UI event listeners
    setupHeaderControls();
    setupPresetButtons();
    setupFormHandlers();

    // 3. Check API health and fetch metadata
    await verifyApiHealth();
    await loadInitialData();
});

function setupHeaderControls() {
    // Theme toggle button
    const themeBtn = document.getElementById("themeToggleBtn");
    if (themeBtn) {
        themeBtn.addEventListener("click", () => {
            themeManager.toggleTheme();
        });
    }

    // Language toggle button
    const langBtn = document.getElementById("langToggleBtn");
    if (langBtn) {
        langBtn.addEventListener("click", () => {
            i18n.toggleLanguage();
            // Re-render prediction results with new language if present
            if (window.lastPredictionData) {
                renderPredictionResult(window.lastPredictionData);
            }
        });
    }
}

async function verifyApiHealth() {
    const badge = document.getElementById("apiStatusBadge");
    const dot = document.getElementById("apiStatusDot");
    const text = document.getElementById("apiStatusText");

    if (!badge || !dot || !text) return;

    text.textContent = i18n.t("status_checking");

    const health = await apiClient.checkHealth();
    if (health.ok && health.data.service_ready) {
        dot.className = "status-dot online";
        text.textContent = i18n.t("status_online");
        badge.classList.remove("offline", "degraded");
        badge.classList.add("online");
    } else if (health.ok) {
        dot.className = "status-dot degraded";
        text.textContent = i18n.t("status_degraded");
        badge.classList.remove("online", "offline");
        badge.classList.add("degraded");
    } else {
        dot.className = "status-dot offline";
        text.textContent = i18n.t("status_offline");
        badge.classList.remove("online", "degraded");
        badge.classList.add("offline");
    }
}

async function loadInitialData() {
    // Fetch real sample records
    const samples = await apiClient.getSampleRecords();
    if (samples && samples.length) {
        window.samplePresets = samples;
    }

    // Fetch historical stats for charts
    const hist = await apiClient.getHistoricalStats();
    const modelInfo = await apiClient.getModelInfo();
    if (hist && hist.stats) {
        analyticsCharts.setData(hist.stats, modelInfo?.feature_importance || null);
    }
}

function setupPresetButtons() {
    const presetButtons = document.querySelectorAll(".preset-btn");
    presetButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const presetType = btn.getAttribute("data-preset");
            loadPreset(presetType);
        });
    });
}

function loadPreset(type) {
    // Verified authentic presets from Beijing combined dataset
    const presets = {
        clean: {
            year: 2014,
            month: 4,
            day: 5,
            hour: 11,
            DEWP: -18.0,
            TEMP: 16.0,
            PRES: 1024.0,
            station: "US_Embassy"
        },
        moderate: {
            year: 2012,
            month: 7,
            day: 24,
            hour: 5,
            DEWP: 21.0,
            TEMP: 23.0,
            PRES: 1008.0,
            station: "US_Embassy"
        },
        heavy: {
            year: 2014,
            month: 10,
            day: 20,
            hour: 20,
            DEWP: 14.2,
            TEMP: 16.9,
            PRES: 1016.4,
            station: "Aotizhongxin"
        }
    };

    const target = presets[type];
    if (!target) return;

    // Fill form fields
    Object.keys(target).forEach(field => {
        const input = document.getElementById(`field_${field}`);
        if (input) {
            input.value = target[field];
            input.classList.remove("is-invalid");
        }
    });

    // Clear previous error messages
    hideFormAlert();
}

function setupFormHandlers() {
    const form = document.getElementById("predictionForm");
    const resetBtn = document.getElementById("resetBtn");

    if (resetBtn) {
        resetBtn.addEventListener("click", () => {
            form.reset();
            loadPreset("moderate");
            hideFormAlert();
        });
    }

    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            await handleFormSubmit();
        });
    }
}

function getFormData() {
    const stationVal = document.getElementById("field_station")?.value || "US_Embassy";
    const isAoti = stationVal === "Aotizhongxin";

    return {
        year: parseInt(document.getElementById("field_year")?.value, 10),
        month: parseInt(document.getElementById("field_month")?.value, 10),
        day: parseInt(document.getElementById("field_day")?.value, 10),
        hour: parseInt(document.getElementById("field_hour")?.value, 10),
        DEWP: parseFloat(document.getElementById("field_DEWP")?.value),
        TEMP: parseFloat(document.getElementById("field_TEMP")?.value),
        PRES: parseFloat(document.getElementById("field_PRES")?.value),
        station: stationVal,
        station_Aotizhongxin: isAoti ? 1.0 : 0.0,
        station_US_Embassy: isAoti ? 0.0 : 1.0
    };
}

function validateFormData(data) {
    const errors = [];

    if (isNaN(data.year) || data.year < 2000 || data.year > 2100) {
        errors.push({ field: "year", msg: "Year must be between 2000 and 2100" });
    }
    if (isNaN(data.month) || data.month < 1 || data.month > 12) {
        errors.push({ field: "month", msg: "Month must be between 1 and 12" });
    }
    if (isNaN(data.day) || data.day < 1 || data.day > 31) {
        errors.push({ field: "day", msg: "Day must be between 1 and 31" });
    }
    if (isNaN(data.hour) || data.hour < 0 || data.hour > 23) {
        errors.push({ field: "hour", msg: "Hour must be between 0 and 23" });
    }
    if (isNaN(data.DEWP) || data.DEWP < -60 || data.DEWP > 50) {
        errors.push({ field: "DEWP", msg: "Dew point must be between -60°C and 50°C" });
    }
    if (isNaN(data.TEMP) || data.TEMP < -50 || data.TEMP > 60) {
        errors.push({ field: "TEMP", msg: "Temperature must be between -50°C and 60°C" });
    }
    if (isNaN(data.PRES) || data.PRES < 900 || data.PRES > 1100) {
        errors.push({ field: "PRES", msg: "Pressure must be between 900 and 1100 hPa" });
    }
    if (!["US_Embassy", "Aotizhongxin"].includes(data.station)) {
        errors.push({ field: "station", msg: "Station must be US_Embassy or Aotizhongxin" });
    }

    return errors;
}

async function handleFormSubmit() {
    hideFormAlert();

    const data = getFormData();
    const errors = validateFormData(data);

    // Clear previous input error styles
    document.querySelectorAll(".form-input, .form-select").forEach(el => el.classList.remove("is-invalid"));

    if (errors.length > 0) {
        errors.forEach(err => {
            const el = document.getElementById(`field_${err.field}`);
            if (el) el.classList.add("is-invalid");
        });
        showFormAlert(errors[0].msg);
        return;
    }

    // Set loading state on button
    setButtonLoading(true);

    try {
        const response = await apiClient.predict(data);

        if (!response.ok) {
            showFormAlert(response.error || i18n.t("val_network_error"));
            return;
        }

        // Store result for language/theme switch re-render
        window.lastPredictionData = response.data;
        renderPredictionResult(response.data);

    } catch (err) {
        showFormAlert(i18n.t("val_network_error"));
    } finally {
        setButtonLoading(false);
    }
}

function setButtonLoading(isLoading) {
    const btn = document.getElementById("predictBtn");
    if (!btn) return;

    const btnText = btn.querySelector(".btn-text");
    const spinner = btn.querySelector(".btn-spinner");

    if (isLoading) {
        btn.disabled = true;
        if (btnText) btnText.textContent = i18n.t("btn_predicting");
        if (spinner) spinner.classList.remove("hidden");
    } else {
        btn.disabled = false;
        if (btnText) btnText.textContent = i18n.t("btn_predict");
        if (spinner) spinner.classList.add("hidden");
    }
}

function showFormAlert(message) {
    const alertBox = document.getElementById("formAlert");
    if (!alertBox) return;
    alertBox.textContent = message;
    alertBox.classList.remove("hidden");
}

function hideFormAlert() {
    const alertBox = document.getElementById("formAlert");
    if (alertBox) alertBox.classList.add("hidden");
}

function renderPredictionResult(result) {
    const placeholder = document.getElementById("resultPlaceholder");
    const content = document.getElementById("resultContent");

    if (placeholder) placeholder.classList.add("hidden");
    if (content) content.classList.remove("hidden");

    // Value display
    const valEl = document.getElementById("resultPm25Value");
    if (valEl) {
        animateCounter(valEl, result.predicted_pm25);
    }

    // Latency and model badge
    const latencyEl = document.getElementById("resultLatency");
    if (latencyEl) {
        latencyEl.textContent = `${result.execution_time_ms} ms`;
    }

    const timeEl = document.getElementById("resultTimestamp");
    if (timeEl) {
        timeEl.textContent = new Date(result.timestamp).toLocaleTimeString();
    }

    // Visual gauge / scale indicator
    const scaleBar = document.getElementById("resultScaleBar");
    if (scaleBar) {
        const pct = Math.min(100, (result.predicted_pm25 / 300) * 100);
        scaleBar.style.width = `${pct}%`;
    }

    // Echoed inputs list
    const inputsList = document.getElementById("resultInputsSummary");
    if (inputsList && result.input_features) {
        inputsList.innerHTML = "";
        const f = result.input_features;
        const stationLabel = f.station === "Aotizhongxin" ? i18n.t("station_aoti") : i18n.t("station_usembassy");

        const items = [
            { label: i18n.t("field_year"), val: f.year },
            { label: i18n.t("field_month"), val: f.month },
            { label: i18n.t("field_day"), val: f.day },
            { label: i18n.t("field_hour"), val: `${f.hour}:00` },
            { label: i18n.t("field_dewp"), val: `${f.DEWP} °C` },
            { label: i18n.t("field_temp"), val: `${f.TEMP} °C` },
            { label: i18n.t("field_pres"), val: `${f.PRES} hPa` },
            { label: i18n.t("field_station"), val: stationLabel }
        ];

        items.forEach(it => {
            const pill = document.createElement("span");
            pill.className = "input-summary-pill";
            pill.innerHTML = `<strong>${it.label}:</strong> ${it.val}`;
            inputsList.appendChild(pill);
        });
    }
}

function animateCounter(element, targetValue) {
    const duration = 600;
    const startValue = 0;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easeOutQuad = 1 - (1 - progress) * (1 - progress);
        const current = startValue + (targetValue - startValue) * easeOutQuad;

        element.textContent = current.toFixed(2);

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = targetValue.toFixed(2);
        }
    }

    requestAnimationFrame(update);
}
