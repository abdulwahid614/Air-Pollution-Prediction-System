/**
 * Internationalization (i18n) module for Air Pollution Prediction System.
 * Supports complete English (LTR) and Arabic (RTL) switching with persistent storage.
 */

const translations = {
    en: {
        // App Header
        app_title: "AeroPredict",
        app_subtitle: "Air Pollution PM2.5 Prediction System",
        nav_dashboard: "Dashboard",
        nav_predict: "Predict",
        nav_analytics: "Analytics",
        nav_model_info: "Model Info",
        nav_api_docs: "API Docs",
        theme_toggle_label: "Toggle Dark/Light Mode",
        lang_toggle_label: "تغيير للغة العربية",
        lang_current: "English",

        // Health Status
        status_checking: "Checking service...",
        status_online: "API Online & Model Ready",
        status_degraded: "Service Degraded",
        status_offline: "API Offline",

        // Intro / Banner
        hero_badge: "XGBoost Machine Learning Pipeline",
        hero_title: "Meteorological Air Quality Predictor",
        hero_desc: "Estimates fine particulate matter (PM2.5 concentration in µg/m³) based on atmospheric conditions, barometric pressure, dew point, temperature, and monitoring station location.",

        // KPI Cards
        kpi_target: "Target Variable",
        kpi_target_val: "PM2.5 (µg/m³)",
        kpi_target_sub: "Fine Particulate Matter",
        kpi_model: "Trained Algorithm",
        kpi_model_val: "XGBoost Regressor",
        kpi_model_sub: "500 Estimators • Depth 4",
        kpi_rmse: "Holdout RMSE",
        kpi_rmse_val: "61.62 µg/m³",
        kpi_rmse_sub: "Verified on 20% Test Set",
        kpi_mae: "Holdout MAE",
        kpi_mae_val: "42.95 µg/m³",
        kpi_mae_sub: "Mean Absolute Error",

        // Form Section
        form_title: "Environmental & Temporal Inputs",
        form_subtitle: "Enter meteorological parameters or select an authentic historical preset",
        preset_label: "Load Verified Historical Sample:",
        preset_clean: "Clean Air (US Embassy)",
        preset_moderate: "Moderate Air (US Embassy)",
        preset_heavy: "Severe Pollution (Aotizhongxin)",

        // Form Fields
        field_group_time: "Observation Date & Time",
        field_year: "Year",
        field_year_help: "Recorded observation year",
        field_month: "Month",
        field_month_help: "Month of observation (1 to 12)",
        field_day: "Day",
        field_day_help: "Day of the month (1 to 31)",
        field_hour: "Hour",
        field_hour_help: "Hour of day (00:00 to 23:00)",

        field_group_weather: "Atmospheric Measurements",
        field_dewp: "Dew Point (DEWP)",
        field_dewp_unit: "°C",
        field_dewp_help: "Atmospheric dew point temperature",
        field_temp: "Ambient Temperature (TEMP)",
        field_temp_unit: "°C",
        field_temp_help: "Ground-level air temperature",
        field_pres: "Barometric Pressure (PRES)",
        field_pres_unit: "hPa",
        field_pres_help: "Sea-level equivalent pressure",

        field_group_station: "Air Quality Monitoring Station",
        field_station: "Select Monitoring Station",
        field_station_help: "Observation source for PM2.5 measurement",
        station_usembassy: "US Embassy (السفارة الأمريكية)",
        station_aoti: "Aotizhongxin (أوتيتشونغشين)",

        // Form Actions
        btn_predict: "Predict PM2.5 Concentration",
        btn_predicting: "Calculating Prediction...",
        btn_reset: "Reset Form",

        // Validation & Alerts
        val_required: "This field is required",
        val_range: "Value must be between {min} and {max}",
        val_invalid: "Invalid input value",
        val_error_title: "Validation Error",
        val_network_error: "Could not connect to the API. Ensure server is running.",

        // Prediction Results
        result_title: "Prediction Result",
        result_placeholder_title: "Awaiting Input",
        result_placeholder_desc: "Configure meteorological parameters on the left and click 'Predict PM2.5 Concentration' to run the model.",
        result_target_label: "Predicted Pollutant Concentration",
        result_target_name: "PM2.5 (Fine Particulate Matter)",
        result_unit: "µg/m³",
        result_model_badge: "XGBoost Regression Model",
        result_time_label: "Latency:",
        result_timestamp_label: "Time:",
        result_inputs_summary: "Processed Input Summary",

        // Analytics & Visualizations
        analytics_title: "Dataset Insights & Model Analytics",
        analytics_subtitle: "Verified statistics extracted from the Beijing Combined dataset and trained XGBoost model",
        tab_monthly: "Monthly PM2.5 Cycle",
        tab_hourly: "Diurnal Pollution Curve",
        tab_importance: "Feature Importance",

        // Model Architecture Specifications
        specs_dataset: "Dataset: Beijing PM2.5 Combined Dataset (US Embassy & Aotizhongxin)",
        specs_samples: "Total Evaluated Records: 75,896 clean observations",
        specs_split: "Validation Split: 80% Chronological Train / 20% Holdout Test",
        specs_algorithm: "Algorithm: Extreme Gradient Boosting (XGBoost)",
        specs_objective: "Loss Function: reg:squarederror (RMSE)",
        specs_features_count: "Total Processed Features: 9 columns (One-Hot Encoded station)",

        // Footer
        footer_text: "Air Pollution PM2.5 Prediction System • Powered by FastAPI & XGBoost",
        footer_docs_link: "Interactive Swagger API Docs"
    },

    ar: {
        // App Header
        app_title: "AeroPredict",
        app_subtitle: "نظام التنبؤ بتلوث الهواء والجسيمات الدقيقة PM2.5",
        nav_dashboard: "لوحة التحكم",
        nav_predict: "التنبؤ",
        nav_analytics: "التحليلات",
        nav_model_info: "معلومات النموذج",
        nav_api_docs: "توثيق API",
        theme_toggle_label: "تبديل المظهر الداكن/الفاتح",
        lang_toggle_label: "Switch to English",
        lang_current: "العربية",

        // Health Status
        status_checking: "جاري فحص الخدمة...",
        status_online: "واجهة API متصلة والنموذج جاهز",
        status_degraded: "الخدمة تعمل جزئياً",
        status_offline: "واجهة API غير متصلة",

        // Intro / Banner
        hero_badge: "خط معالجة تعلم الآلة بواسطة XGBoost",
        hero_title: "متنبئ جودة الهواء والظروف الجوية",
        hero_desc: "تقدير تركيز الجسيمات الدقيقة العالقة (PM2.5 بالميكروغرام/متر مكعب) بناءً على المؤشرات الجوية، والضغط الجوي، ونقطة الندى، ودرجة الحرارة، ومحطة الرصد.",

        // KPI Cards
        kpi_target: "المتغير المستهدف",
        kpi_target_val: "PM2.5 (ميكروغرام/م³)",
        kpi_target_sub: "الجسيمات الدقيقة العالقة",
        kpi_model: "النموذج المدرب",
        kpi_model_val: "انحدار XGBoost",
        kpi_model_sub: "500 شجرة • أقصى عمق 4",
        kpi_rmse: "جذر متوسط مربع الخطأ (RMSE)",
        kpi_rmse_val: "61.62 ميكروغرام/م³",
        kpi_rmse_sub: "تم التحقق على 20% بيانات اختبار",
        kpi_mae: "متوسط الخطأ المطلق (MAE)",
        kpi_mae_val: "42.95 ميكروغرام/م³",
        kpi_mae_sub: "دقة التنبؤ على الاختبار",

        // Form Section
        form_title: "المدخلات البيئية والزمنية",
        form_subtitle: "أدخل المؤشرات الجوية أو اختر عينة تاريخية حقيقية للتحقق الفوري",
        preset_label: "تحميل عينة تاريخية موثقة:",
        preset_clean: "هواء نقي (السفارة الأمريكية)",
        preset_moderate: "تلوث معتدل (السفارة الأمريكية)",
        preset_heavy: "تلوث شديد (أوتيتشونغشين)",

        // Form Fields
        field_group_time: "تاريخ ووقت الرصد",
        field_year: "السنة",
        field_year_help: "سنة الرصد المسجلة",
        field_month: "الشهر",
        field_month_help: "شهر الرصد (من 1 إلى 12)",
        field_day: "اليوم",
        field_day_help: "يوم الشهر (من 1 إلى 31)",
        field_hour: "الساعة",
        field_hour_help: "ساعة اليوم بنظام 24 ساعة (0 إلى 23)",

        field_group_weather: "القياسات الجوية والطقس",
        field_dewp: "نقطة الندى (DEWP)",
        field_dewp_unit: "°م",
        field_dewp_help: "درجة حرارة نقطة الندى الجوية",
        field_temp: "درجة الحرارة (TEMP)",
        field_temp_unit: "°م",
        field_temp_help: "درجة حرارة الهواء السطحي",
        field_pres: "الضغط الجوي (PRES)",
        field_pres_unit: "هكتوباسكال",
        field_pres_help: "الضغط الجوي المعادل لمستوى سطح البحر",

        field_group_station: "محطة رصد جودة الهواء",
        field_station: "اختيار محطة الرصد",
        field_station_help: "المحطة المسؤولة عن تسجيل قياسات التلوث",
        station_usembassy: "السفارة الأمريكية (US Embassy)",
        station_aoti: "أوتيتشونغشين (Aotizhongxin)",

        // Form Actions
        btn_predict: "حساب التنبؤ بتركيز PM2.5",
        btn_predicting: "جاري تشغيل النموذج...",
        btn_reset: "إعادة تعيين النموذج",

        // Validation & Alerts
        val_required: "هذا الحقل مطلوب",
        val_range: "القيمة يجب أن تكون بين {min} و {max}",
        val_invalid: "قيمة غير صالحة",
        val_error_title: "خطأ في التحقق من البيانات",
        val_network_error: "تعذر الاتصال بواجهة برمجة التطبيقات (API). يرجى التأكد من تشغيل الخادم.",

        // Prediction Results
        result_title: "نتيجة التنبؤ",
        result_placeholder_title: "في انتظار إدخال البيانات",
        result_placeholder_desc: "قم بتعبئة القياسات الجوية على اليمين ثم اضغط على زر 'حساب التنبؤ بتركيز PM2.5' لتشغيل النموذج.",
        result_target_label: "تركيز الملوثات المتوقع",
        result_target_name: "PM2.5 (الجسيمات الدقيقة العالقة)",
        result_unit: "ميكروغرام/م³",
        result_model_badge: "نموذج انحدار XGBoost",
        result_time_label: "زمن الاستجابة والاستدلال",
        result_timestamp_label: "وقت الرصد",
        result_inputs_summary: "ملخص المدخلات المعالجة",

        // Analytics & Visualizations
        analytics_title: "تحليلات البيانات وإحصائيات النموذج",
        analytics_subtitle: "إحصائيات موثقة مستخرجة من مجموعة بيانات بكين المدمجة ونموذج XGBoost",
        tab_monthly: "الدورة الشهرية لتلوث PM2.5",
        tab_hourly: "المنحنى اليومي للتلوث خلال 24 ساعة",
        tab_importance: "أهمية المتغيرات",

        // Model Architecture Specifications
        specs_dataset: "مصدر البيانات: مجموعة بيانات بكين المدمجة (السفارة الأمريكية وأوتيتشونغشين)",
        specs_samples: "إجمالي السجلات المفحوصة: 75,896 سجلاً جوياً نظيفاً",
        specs_split: "نسبة التحقق: 80% تدريب زمني / 20% اختبار مستقل",
        specs_algorithm: "الخوارزمية: التدرج التعزيزي الشديد (XGBoost)",
        specs_objective: "دالة الخسارة: خطأ المتوسط التربيعي (RMSE)",
        specs_features_count: "إجمالي الخصائص المعالجة: 9 أعمدة (ترميز One-Hot للمحطة)",

        // Footer
        footer_text: "نظام التنبؤ بتلوث الهواء PM2.5 • مبني بواسطة FastAPI و XGBoost",
        footer_docs_link: "توثيق واجهة API التفاعلية (Swagger)"
    }
};

class I18nManager {
    constructor() {
        this.currentLang = this.getInitialLanguage();
    }

    getInitialLanguage() {
        const saved = localStorage.getItem("app_language");
        if (saved && (saved === "en" || saved === "ar")) {
            return saved;
        }
        return "ar";
    }

    getLanguage() {
        return this.currentLang;
    }

    setLanguage(lang) {
        if (lang !== "en" && lang !== "ar") return;
        this.currentLang = lang;
        localStorage.setItem("app_language", lang);

        // Apply HTML dir and lang attributes
        document.documentElement.lang = lang;
        document.documentElement.dir = (lang === "ar") ? "rtl" : "ltr";

        // Update current lang label
        const currentLangLabel = document.getElementById("currentLangLabel");
        if (currentLangLabel) {
            currentLangLabel.textContent = (lang === "ar") ? "English" : "العربية";
        }

        // Update all translated elements in DOM
        this.updateDOM();

        // Dispatch custom event for charts and dynamic components
        window.dispatchEvent(new CustomEvent("languageChanged", {
            detail: { language: lang, isRTL: lang === "ar" }
        }));
    }

    toggleLanguage() {
        const newLang = (this.currentLang === "en") ? "ar" : "en";
        this.setLanguage(newLang);
    }

    t(key, params = {}) {
        const langDict = translations[this.currentLang] || translations.en;
        let text = langDict[key] || translations.en[key] || key;

        // Replace interpolation parameters like {min}, {max}
        Object.keys(params).forEach(k => {
            text = text.replace(new RegExp(`\\{${k}\\}`, "g"), params[k]);
        });
        return text;
    }

    updateDOM() {
        document.querySelectorAll("[data-i18n]").forEach(el => {
            const key = el.getAttribute("data-i18n");
            el.textContent = this.t(key);
        });

        document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
            const key = el.getAttribute("data-i18n-placeholder");
            el.setAttribute("placeholder", this.t(key));
        });

        document.querySelectorAll("[data-i18n-title]").forEach(el => {
            const key = el.getAttribute("data-i18n-title");
            el.setAttribute("title", this.t(key));
        });

        document.querySelectorAll("[data-i18n-aria]").forEach(el => {
            const key = el.getAttribute("data-i18n-aria");
            el.setAttribute("aria-label", this.t(key));
        });
    }

    init() {
        document.documentElement.lang = this.currentLang;
        document.documentElement.dir = (this.currentLang === "ar") ? "rtl" : "ltr";
        const currentLangLabel = document.getElementById("currentLangLabel");
        if (currentLangLabel) {
            currentLangLabel.textContent = (this.currentLang === "ar") ? "English" : "العربية";
        }
        this.updateDOM();
    }
}

const i18n = new I18nManager();
window.i18n = i18n;
