/**
 * Theme manager for Air Pollution Prediction System.
 * Supports smooth Dark and Light modes with local persistence and system detection.
 */

class ThemeManager {
    constructor() {
        this.currentTheme = this.getInitialTheme();
    }

    getInitialTheme() {
        const saved = localStorage.getItem("app_theme");
        if (saved && (saved === "dark" || saved === "light")) {
            return saved;
        }
        if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
            return "dark";
        }
        return "light";
    }

    getTheme() {
        return this.currentTheme;
    }

    setTheme(theme) {
        if (theme !== "dark" && theme !== "light") return;
        this.currentTheme = theme;
        localStorage.setItem("app_theme", theme);
        document.documentElement.setAttribute("data-theme", theme);

        // Update theme toggle icon if present
        this.updateThemeButton();

        // Dispatch custom event for charts and interactive widgets
        window.dispatchEvent(new CustomEvent("themeChanged", {
            detail: { theme: theme, isDark: theme === "dark" }
        }));
    }

    toggleTheme() {
        const nextTheme = (this.currentTheme === "dark") ? "light" : "dark";
        this.setTheme(nextTheme);
    }

    updateThemeButton() {
        const btn = document.getElementById("themeToggleBtn");
        if (!btn) return;
        const icon = btn.querySelector(".theme-icon");
        if (icon) {
            icon.textContent = (this.currentTheme === "dark") ? "☀️" : "🌙";
        }
    }

    init() {
        document.documentElement.setAttribute("data-theme", this.currentTheme);
        this.updateThemeButton();

        // Listen for OS theme changes if user has not set a preference
        if (window.matchMedia) {
            window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
                if (!localStorage.getItem("app_theme")) {
                    this.setTheme(e.matches ? "dark" : "light");
                }
            });
        }
    }
}

const themeManager = new ThemeManager();
window.themeManager = themeManager;
