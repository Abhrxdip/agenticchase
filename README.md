# AgenticAvocado 🥑

An autonomous agent framework designed to plan, retrieve context, and execute multi-step workflows with tool-calling capabilities. Built from scratch by **Team Avocado**.

---

## ⚡ What it Does

Most simple LLM wrappers fail when tasks require sustained context and sequential decision-making. `AgenticAvocado` implements an iterative think-plan-act loop:

1. **Task Decomposition:** Breaks down ambiguous user queries into atomic steps.
2. **Context & Memory:** Retains working memory across reasoning traces without blowing token limits.
3. **Tool Execution:** Interfaces with local utilities and APIs dynamically to gather real-world data.
4. **Self-Correction:** Inspects intermediate tool outputs and adjusts parameters if a step fails.

---

## 🏗️ Architecture

```text
User Prompt
│
▼
[ Orchestrator ] ◄───► [ Memory Buffer ]
│
├─► [ Step Planner ]
│        │
│        ▼
├─► [ Tool Router / Registry ]
│        ├── Web / Search
│        ├── Code / Shell Runner
│        └── File & Vector Ops
│
▼
Synthesized Result
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (or Node.js 18+ depending on your runtime)
- Git

### 2. Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/Abhrxdip/agenticchase.git
cd agenticchase
```

Set up environment variables:

```bash
cp sample.env .env
# Open .env and insert your API keys & runtime configurations
```

Install packages:

```bash
# If Python:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or using uv:
uv sync
```

### 3. Usage
Run the agent CLI or consultation interface:

```bash
python main.py
```

---

## 🛠️ Roadmap & Progress
- [x] Core agent loop and state interface
- [x] Vision & multimodal input processing
- [x] Voice transcription and speech generation
- [x] Interactive web consultation interface
- [ ] Multi-agent collaboration protocols
- [ ] Persistent vector memory integration

---

## 👥 Authors
Developed by **Abhradip** for **Team Avocado**.
