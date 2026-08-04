# Alexander OS (v1.0 — Prototype)

**Offline AI Tutoring for High School Students. No internet. No subscription. Runs on the Android phone you already own.**

---

## The Problem

I faced this myself in 11th and 12th grade. I knew AI could help me study — but every tool had a usage limit, and it would run out mid-session, right when I needed it most. I'm in college now with a free Gemini Pro plan, but that access came too late to help me when I actually needed it.

Across India, millions of high schoolers are in the same spot: no money for tuition, patchy or no internet, and AI tools that cut them off right when studying gets hard. Private coaching costs ₹1–3 lakh per year — completely out of reach for most families.

AI tutors exist. But nearly every one requires cloud APIs, subscriptions, and stable broadband. The moment the internet drops — which it does, constantly, in rural and semi-urban India — the tutor disappears. The students who need help the most are the ones who get cut off.

**Alexander OS is built for those students.** It runs the entire AI tutoring stack on-device. No API calls. No server. No connectivity required. A student can ask a question and get a clear, step-by-step explanation in seconds, even with zero internet. This is not a feature. It is the point.

---

## What It Does

Alexander is a Socratic AI tutor that runs fully offline on entry-level Android phones. The system routes queries intelligently between two locally-running models:

- **STEM queries** (solve, calculate, derive, formula, force, friction...) → routed to `deepseek-r1:1.5b`, a 1.5B parameter reasoning model distilled from the Qwen architecture, optimized for mathematical chain-of-thought.
- **General queries** (explanations, conceptual questions, reading comprehension) → routed to `gemma:2b`, Google's 2B parameter general-purpose model.

Both models run via **Ollama** on the local machine (desktop demo) or via **llama.cpp** for Android compatibility. A Flask-based kernel orchestrator handles routing, RAG context injection from local JSON/PDF textbook data, and streaming response delivery to the frontend.

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
      │       └── chapter2.json → inject textbook page context if keyword match
      │
      └── Ollama / llama.cpp (localhost:11434)
              └── Streamed token response → Frontend
```

**Cold-Swap Memory Logic:** Models are not kept simultaneously in RAM. The kernel loads only the active model on demand, swapping it out when the next query requires the other. This prevents OOM crashes on Android phones with limited unified memory.

**Zero Network Dependency:** The inference endpoint is `localhost`. The student's device is the server.

**Privacy by architecture:** No student query, no personal data, and no academic content ever leaves the device. This is not a policy — it is a technical guarantee baked into the system design.

**Textbook-Grounded RAG:** Every answer is checked against the student's own textbook content before being shown, so the tutor explains within the syllabus instead of hallucinating facts that aren't there.

---

## Why This Needs to Exist

AI tutoring already exists — but almost all of it depends on cloud APIs, subscriptions, and stable internet. The moment connectivity drops or a usage limit is hit, the help disappears. For a student in a small town or without reliable data, that's not an edge case — it's most days.

Alexander OS flips that: the phone itself is the tutor. No recurring cost, no dependence on network quality, no cutoff mid-problem. A student in a village with a basic Android phone should have the same access to a patient, knowledgeable tutor as a student paying lakhs for coaching. That gap is a solvable engineering problem. Alexander OS is the solution.

---

## Distribution

Alexander OS will launch on the Play Store, so students can find and download it directly — no institutional gatekeeping, no school procurement process required. Alongside the public launch, I'm running a pilot with 2–3 schools to get the app in front of real students, gather feedback, and validate that it actually helps with real studying, not just in a demo.

---

## Current Status

- ✅ Working prototype — Flask kernel + Ollama + dual-model routing
- ✅ Local RAG from textbook data (`chapter2.json`)
- ✅ Streaming responses with LaTeX formula support
- 🔄 Android port in progress — porting inference layer from Ollama to `llama.cpp` for full Android compatibility
- 🔄 Preparing Play Store launch
- 🔄 Multi-subject expansion: Physics, Chemistry, Hindi language support
- 🔄 Pilot planned with 2–3 schools

---

## Tech Stack

| Layer                  | Technology                                       |
| ----------------------- | ------------------------------------------------ |
| Backend Kernel         | Python + Flask                                   |
| Local Inference        | Ollama / llama.cpp                               |
| STEM Model             | `deepseek-r1:1.5b` (Qwen-distilled, 1.5B params) |
| General Model          | `gemma:2b` (Google Gemma, 2B params)              |
| Android Target Runtime | llama.cpp (JNI bridge)                           |
| RAG Source             | Local JSON / sideloaded PDFs                     |
| Frontend               | HTML/CSS/JS (streamed responses)                 |
| Hardware Target        | Entry-level Android phones                       |

---

## Why Now

Three things converged that make this the right moment:

1. **Small language models got genuinely capable.** DeepSeek R1 1.5B can solve high school physics. Gemma 2B can explain concepts clearly. This quality wasn't possible at sub-2B parameters until recently.

2. **The hardware already exists.** Most Indian students already own or have access to a basic Android phone — the same device they use for everything else. The distribution problem is solved. The software problem is not.

3. **Cloud-dependent AI is widening the gap.** Every AI tutoring product that requires broadband and a subscription makes the divide between connected and unconnected students worse. Alexander OS goes in the opposite direction, deliberately.

---

## Who Built This

Varun Jarwani — 18, Ahmedabad, India. Self-taught since 6th grade, learned entirely through building and GitHub, no bootcamps. Ranked 10th globally in a coding competition in 8th grade.

I lived the exact gap Alexander OS is meant to close — running out of AI access mid-study in 11th and 12th grade, with no one around to help. I'm building this because I want the next student in my position to have a tutor that doesn't run out on them.

**GitHub:** [github.com/varunjarwani-max/alexander-os-v2](https://github.com/varunjarwani-max/alexander-os-v2)
