# Alexander OS (v1.0 — Prototype)

**Offline AI Tutoring for K-12. No internet. No subscription. Runs on a ₹12,000 Android tablet.**

---

## The Problem

Across India, 250 million school-age students prepare for board exams and competitive entrance tests without access to quality tutoring. Private coaching costs ₹1–3 lakh per year — completely out of reach for the majority of families. In the US, private tutoring runs $2,000–5,000 per year per student.

AI tutors exist. But every single one requires cloud APIs, subscriptions, and stable broadband. The moment the internet drops — which it does, constantly, in rural and semi-urban India — the tutor disappears. The students who need help the most are the ones who get cut off.

**Alexander OS is built for those students.** It runs the entire AI tutoring stack on-device. No API calls. No server. No connectivity required. A student in a village with no WiFi can photograph a textbook problem and receive a spoken, step-by-step explanation in seconds. This is not a feature. It is the point.

---

## What It Does

Alexander is a Socratic AI tutor that runs fully offline on entry-level Android tablets (4GB RAM). The system routes queries intelligently between two locally-running models:

- **STEM queries** (solve, calculate, derive, formula, force, friction...) → routed to `deepseek-r1:1.5b`, a 1.5B parameter reasoning model distilled from the Qwen architecture, optimized for mathematical chain-of-thought.
- **General queries** (explanations, conceptual questions, reading comprehension) → routed to `gemma:2b`, Google's 2B parameter general-purpose model.

Both models run via **Ollama** on the local machine (Windows/Mac demo) or via **llama.cpp** for Android compatibility. A Flask-based kernel orchestrator handles routing, RAG context injection from local JSON/PDF textbook data, and streaming response delivery to the frontend.

---

## Architecture

```
Student Query
      │
      ▼
Flask Kernel (ui.py)
      │
      ├── Keyword Router
      │       ├── STEM? → deepseek-r1:1.5b  (Reasoning / Math)
      │       └── General? → gemma:2b        (Explanation / Concept)
      │
      ├── Local RAG
      │       └── chapter2.json → inject PDF page context if keyword match
      │
      └── Ollama / llama.cpp (localhost:11434)
              └── Streamed token response → Frontend
```

**Cold-Swap Memory Logic:** Models are not kept simultaneously in RAM. The kernel loads only the active model on demand, swapping it out when the next query requires the other. This prevents OOM crashes on Android tablets with 4GB of unified memory.

**Zero Network Dependency:** The inference endpoint is `localhost`. The student's device is the server.

**Privacy by architecture:** No student query, no personal data, and no academic content ever leaves the device. This is not a policy — it is a technical guarantee baked into the system design.

---

## Why This Needs to Exist

India's NAMO E-Tablet Yojana distributes Acer and Lenovo Android tablets to 3 lakh students annually at ₹1,000. These devices already exist. They are already in students' hands in Gujarat government schools. But there is no software on them capable of replacing a tutor.

Alexander OS is the software layer on top of infrastructure the government is already funding. The tablet problem is solved. We solve the tutoring problem.

A government school student in rural Gujarat, preparing for Class 12 board exams alone at night, should have the same access to a patient, knowledgeable tutor as a student in a Kota coaching institute paying ₹2 lakh a year. That gap is a solvable engineering problem. Alexander OS is the solution.

---

## Pricing (Institutional Licensing)

| Market | Current Cost of Quality Tutoring | Alexander OS |
|--------|----------------------------------|--------------|
| India (offline coaching) | ₹1–3 lakh/year per student | **₹1.5 lakh/year per school** |
| US (private tutoring) | $2,000–5,000/year per student | **$1,600/year per school** |

The pricing model is institutional: one license covers an entire school's Android tablet fleet. No per-student fees. No recurring cloud costs. The unit economics improve as hardware gets cheaper, not worse — because there are no API bills.

---

## Current Status

- ✅ Working Windows prototype — Flask kernel + Ollama + dual-model routing
- ✅ Local RAG from JSON textbook data (`chapter2.json`)
- ✅ Streaming responses with LaTeX formula support
- 🔄 Android port in progress — porting inference layer from Ollama to `llama.cpp` for full Android compatibility
- 🔄 Multi-subject expansion: Physics, Chemistry, Hindi language support

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend Kernel | Python + Flask |
| Local Inference | Ollama / llama.cpp |
| STEM Model | `deepseek-r1:1.5b` (Qwen-distilled, 1.5B params) |
| General Model | `gemma:2b` (Google Gemma, 2B params) |
| Android Target Runtime | llama.cpp (JNI bridge) |
| RAG Source | Local JSON / sideloaded PDFs |
| Frontend | HTML/CSS/JS (streamed responses) |
| Hardware Target | Android tablets, 4GB RAM (Acer/Lenovo NAMO E-Tablet) |

---

## Why Now

Three things converged in 2024–25 that make this the right moment:

1. **Small language models got genuinely capable.** DeepSeek R1 1.5B can solve high school physics. Gemma 2B can explain concepts clearly. 18 months ago, this quality wasn't possible at sub-2B parameters.

2. **The hardware already exists at scale.** Gujarat's government tablet scheme places 3 lakh Android devices into student hands annually. The distribution problem is solved. The software problem is not.

3. **Cloud-dependent AI is widening the gap.** Every new AI tutoring product launched in 2024 requires broadband and a subscription. Each one makes the divide between connected and unconnected students worse. Alexander OS goes in the opposite direction deliberately.

---

## Who Built This

Varun Jarwani — 18, Ahmedabad, India. Started coding in 6th grade. Ranked 10th globally in a coding competition in 8th grade. Built the working Alexander OS prototype in 4 days during JEE preparation — facing the same pressure as the students this is built for.

No institutional backing. No funding. Just a laptop, an idea, and the conviction that the student who cannot afford a tutor deserves one anyway.

**GitHub:** [github.com/varunjarwani-max/alexander-os-v2](https://github.com/varunjarwani-max/alexander-os-v2)
