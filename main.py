from pathlib import Path

import gradio as gr

#from brain_of_the_doctor import brain_of_the_doctor
from brain_of_the_doctor_groq import brain_of_the_doctor
from voice_of_the_doctor import convert_text_to_doctor_audio
from voice_of_the_patient import transcribe_patient_voice


APP_TITLE = "AgenticAvocado 🥑 - Autonomous Consultation Agent"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

:root {
    --ais-bg: #f7f9fb;
    --ais-surface: #ffffff;
    --ais-surface-low: #f2f4f6;
    --ais-surface-container: #eceef0;
    --ais-border: #c6c6cd;
    --ais-border-strong: #76777d;
    --ais-text: #191c1e;
    --ais-muted: #45464d;
    --ais-primary: #0051d5;
    --ais-primary-soft: #dbe1ff;
    --ais-primary-active: #316bf3;
    --ais-danger: #ba1a1a;
    --ais-danger-soft: #ffdad6;
    --ais-radius: 16px;
    --body-background-fill: #f7f9fb;
    --body-text-color: #191c1e;
    --background-fill-primary: #ffffff;
    --background-fill-secondary: #f2f4f6;
    --block-background-fill: #ffffff;
    --block-border-color: #c6c6cd;
    --block-info-text-color: #45464d;
    --block-label-background-fill: #ffffff;
    --block-label-border-color: #c6c6cd;
    --block-label-text-color: #45464d;
    --input-background-fill: #ffffff;
    --input-background-fill-focus: #ffffff;
    --input-border-color: #c6c6cd;
    --input-border-color-focus: #316bf3;
    --input-placeholder-color: #76777d;
    --button-primary-background-fill: #316bf3;
    --button-primary-background-fill-hover: #0051d5;
    --button-primary-text-color: #fefcff;
    color-scheme: light;
}

.gradio-container {
    background: var(--ais-bg) !important;
    color: var(--ais-text) !important;
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif !important;
}

.gradio-container,
.gradio-container * {
    color-scheme: light !important;
}

.ais-shell {
    max-width: 1280px;
    margin: 0 auto;
    padding: 28px 40px 40px;
}

.ais-topbar {
    align-items: center;
    background: var(--ais-surface);
    border: 1px solid var(--ais-border);
    border-radius: 20px;
    display: flex;
    justify-content: space-between;
    margin-bottom: 32px;
    padding: 20px 24px;
}

.ais-brand h1 {
    color: var(--ais-text);
    font-size: 24px;
    font-weight: 650;
    letter-spacing: -0.01em;
    line-height: 32px;
    margin: 0;
}

.ais-brand p,
.ais-footer,
.ais-note,
.ais-panel-copy {
    color: var(--ais-muted);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.03em;
    line-height: 16px;
    margin: 4px 0 0;
}

.ais-security {
    align-items: center;
    color: var(--ais-muted);
    display: flex;
    font-size: 12px;
    font-weight: 600;
    gap: 10px;
}

.ais-security span:not(.ais-icon),
.ais-empty strong,
.ais-panel-copy {
    color: var(--ais-muted) !important;
}

.ais-empty strong {
    color: var(--ais-text) !important;
    display: block;
    font-size: 18px;
    font-weight: 650;
    line-height: 28px;
    margin-bottom: 6px;
}

.ais-icon {
    color: var(--ais-primary);
    font-family: 'Material Symbols Outlined';
    font-size: 22px;
    font-variation-settings: 'FILL' 0, 'wght' 450, 'GRAD' 0, 'opsz' 24;
    line-height: 1;
}

.ais-grid {
    align-items: start;
    display: grid;
    gap: 24px;
    grid-template-columns: minmax(0, 5fr) minmax(0, 7fr);
}

.ais-section-title {
    align-items: center;
    display: flex;
    gap: 8px;
    margin: 0 0 14px;
}

.ais-section-title h2 {
    color: var(--ais-text);
    font-size: 24px;
