"""
AgenticAvocado - Autonomous Clinical Triage & Severity Assessment Engine
Developed by Abhradip for Team Avocado (PS 05 - Open Innovation Healthcare)
"""

from typing import Dict, Any, Optional
import os
import json
from groq import Groq


TRIAGE_SYSTEM_PROMPT = """You are an expert clinical triage assistant specializing in dermatological symptom analysis.
Analyze the patient description and visual observations, and provide a structured JSON response with:
1. "severity": One of ["Low (Self-Care/Observation)", "Moderate (Routine Clinical Visit)", "Urgent (Immediate Attention)"]
2. "risk_level": "LOW", "MODERATE", or "HIGH"
3. "observable_features": A list of 2-4 key clinical features observed or described.
4. "potential_considerations": A list of 2-3 benign or common conditions to discuss with a clinician.
5. "recommended_actions": 2-3 immediate, safe recommendations (e.g. avoid picking, keep clean, photograph daily).
6. "clinician_referral": Recommended specialist (e.g., General Practitioner, Dermatologist, Urgent Care).
7. "summary": A concise 2-sentence clinical intake note.

CRITICAL: Return ONLY raw, valid JSON. Do not wrap in markdown codeblocks. Do not include markdown formatting.
"""

def evaluate_triage(
    patient_text: str,
    doctor_response: str,
    has_image: bool = True,
    has_video: bool = False
) -> Dict[str, Any]:
    """
    Evaluates symptoms and recommendations to produce a structured triage report.
    Falls back gracefully to heuristic rules if the LLM is unavailable.
    """
    groq_api_key = os.environ.get("GROQ_API_KEY")
    
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            prompt = (
                f"Patient Reported Symptoms: {patient_text}\n"
                f"Doctor Initial Assessment: {doctor_response}\n"
                f"Visual Input Provided: {'Image' if has_image else 'None'}, Video: {'Yes' if has_video else 'No'}\n"
            )
            
            chat_completion = client.chat.completions.create(
                model=os.environ.get("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
                temperature=0.2,
                max_completion_tokens=600,
                messages=[
                    {"role": "system", "content": TRIAGE_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
            )
            raw_content = chat_completion.choices[0].message.content.strip()
            # Clean possible markdown ticks
            if raw_content.startswith("```"):
                raw_content = raw_content.strip("`").replace("json\n", "", 1).strip()
            
            return json.loads(raw_content)
        except Exception as e:
            print(f"LLM triage evaluation failed, using heuristic fallback: {e}")

    # Rule-based fallback
    lower_text = (patient_text + " " + doctor_response).lower()
    urgent_keywords = ["bleeding", "severe pain", "spreading fast", "fever", "pus", "black spot", "asymmetrical"]
    moderate_keywords = ["itching", "rash", "dryness", "bump", "redness", "scaling", "swelling"]

    if any(k in lower_text for k in urgent_keywords):
        severity = "Urgent (Immediate Attention)"
        risk = "HIGH"
        specialist = "Dermatologist / Urgent Care"
    elif any(k in lower_text for k in moderate_keywords):
        severity = "Moderate (Routine Clinical Visit)"
        risk = "MODERATE"
        specialist = "Dermatologist"
    else:
        severity = "Low (Self-Care/Observation)"
        risk = "LOW"
        specialist = "General Practitioner"

    return {
        "severity": severity,
        "risk_level": risk,
        "observable_features": ["Reported skin variation", "Localized irritation or lesion"],
        "potential_considerations": ["Contact dermatitis", "Mild localized inflammation"],
        "recommended_actions": [
            "Keep the affected area clean and dry",
            "Monitor for changes in size, shape, or color",
            "Avoid scratching or aggressive topicals"
        ],
        "clinician_referral": specialist,
        "summary": "Patient presented localized dermatological symptoms. Recommended for routine professional consultation."
    }


def format_triage_badge_html(triage_data: Dict[str, Any]) -> str:
    """Renders a styled clinical status badge based on triage severity."""
    severity = triage_data.get("severity", "Moderate (Routine Clinical Visit)")
    risk = triage_data.get("risk_level", "MODERATE")
    specialist = triage_data.get("clinician_referral", "Dermatologist")

    if risk == "HIGH":
        bg_color = "#fee2e2"
        border_color = "#ef4444"
        text_color = "#991b1b"
        icon = "emergency"
    elif risk == "LOW":
        bg_color = "#dcfce7"
        border_color = "#22c55e"
        text_color = "#166534"
        icon = "check_circle"
    else:
        bg_color = "#fef3c7"
        border_color = "#f59e0b"
        text_color = "#92400e"
        icon = "warning"

    return f"""
    <div style="background:{bg_color}; border:1.5px solid {border_color}; border-radius:12px; padding:14px 18px; margin-bottom:14px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">
        <div style="display:flex; align-items:center; gap:10px;">
            <span class="material-symbols-outlined" style="color:{text_color}; font-size:26px;">{icon}</span>
            <div>
                <div style="font-size:11px; text-transform:uppercase; letter-spacing:0.05em; font-weight:700; color:{text_color};">Clinical Triage Level</div>
                <div style="font-size:16px; font-weight:700; color:{text_color};">{severity}</div>
            </div>
        </div>
        <div style="background:rgba(255,255,255,0.7); padding:4px 12px; border-radius:999px; font-size:12px; font-weight:600; color:{text_color}; border:1px solid {border_color};">
            Referral: {specialist}
        </div>
    </div>
    """


def format_triage_markdown(triage_data: Dict[str, Any]) -> str:
    """Formats triage data into a clinical intake summary markdown."""
    features = "\n".join([f"- {f}" for f in triage_data.get("observable_features", [])])
    considerations = "\n".join([f"- {c}" for f in triage_data.get("potential_considerations", [])])
    actions = "\n".join([f"{i+1}. {a}" for i, a in enumerate(triage_data.get("recommended_actions", []))])

    return f"""### 📋 Clinical Intake Summary
**Triage Assessment:** {triage_data.get('severity', 'Pending')}  
**Specialist Recommendation:** {triage_data.get('clinician_referral', 'General Practitioner')}

#### 🔍 Observable Features
{features}

#### 💡 Discussion Topics for Clinician
{considerations}

#### ⚡ Immediate Care Guidelines
{actions}

---
*Note: This summary is generated by AgenticAvocado autonomous triage protocols to assist with clinical consultation preparation. It does not constitute formal medical diagnosis.*
"""


