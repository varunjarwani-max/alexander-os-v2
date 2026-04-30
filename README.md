# Alexander OS
### Offline AI Tutoring for Every Student. No Internet. No Subscription. No Compromise.

> A student in a village with no WiFi deserves the same tutor as a student in South Mumbai with three private teachers.

---

## The Problem

Across India, hundreds of millions of students prepare for board exams and JEE with no access to quality tutoring.

- Private tuition costs ₹2,000–10,000 per month — most families cannot afford it
- AI tutoring tools like Khanmigo and Socratic require stable internet and expensive hardware
- In rural India, neither is reliable
- The students who need the most help have the least access to it

**Alexander OS removes every barrier.**

---

## What It Does

A student opens Alexander OS on a basic Android tablet. They photograph a textbook problem. They get a spoken, step-by-step explanation — instantly, offline, for free.

No internet required. No account. No data leaving the device. Ever.

---

## How It Works

Alexander OS runs two AI models simultaneously on a single device using a custom memory architecture built for low-resource hardware.

```
Question comes in (text, image, or voice)
            ↓
    Gemma 4 E2B — Broker Kernel
    Trimodal: handles language, vision, audio
    Routes math queries to specialist
            ↓
    Qwen 3 1.7B — Math Specialist Kernel
    High-accuracy step-by-step calculation
            ↓
    Cold-Swap Memory Manager
    Neither model fully loaded simultaneously
    Stable on 4GB RAM — no crashes
            ↓
        Answer delivered
    Spoken + text, on device, offline
```

### Why Two Models

One large model that handles everything would exceed the RAM of affordable tablets. Most AI apps solve this by requiring expensive hardware or cloud connectivity.

Alexander OS solves it differently — two smaller specialist models, dynamically sharing memory, routing queries between them based on content type. The result is better accuracy than one general model and stable performance on hardware students can actually afford.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Broker kernel | Gemma 4 E2B — trimodal (text, vision, audio) |
| Math specialist | Qwen 3 1.7B |
| Memory management | Custom cold-swap logic |
| Inference engine | Ollama / MLX-LM |
| Backend | Flask (Python) |
| Target hardware | Android tablets 4GB+ RAM |
| Connectivity | Zero — fully offline |

---

## Current Status

| Feature | Status |
|---|---|
| Dual-kernel architecture | ✅ Working |
| Cold-swap memory management | ✅ Working |
| Math query routing to Qwen 3 | ✅ Working |
| General query routing to Gemma 4 | ✅ Working |
| Flask backend + web interface | ✅ Working |
| Voice input and output | ✅ Working |
| Android port (llama.cpp) | 🔄 In progress |
| UI overhaul | 🔄 In progress |
| Google Play Store release | 📅 Month 3 target |

---

## Why Android

India's government tablet distribution schemes place Android devices directly into student hands:

- **NAMO E-Tablet Yojana** — Gujarat government distributes Acer and Lenovo Android tablets to 3 lakh students annually at ₹1,000
- **UP Free Tablet Yojana** — targets 1 crore students across Uttar Pradesh  
- **National Free Tablet Yojana 2025** — 10 lakh college students across India

The government is solving the hardware problem. Alexander OS is the software layer on top of infrastructure already being funded.

---

## Roadmap

| Timeline | Milestone |
|---|---|
| Month 1–2 | Android port complete, UI overhaul, stability hardening |
| Month 3 | Multi-subject support — Physics, Chemistry, Hindi. Play Store release |
| Month 4–5 | Pilot with 2–3 Gujarat government schools. 25 tablets donated to highest-need students |
| Month 6 | Accuracy benchmarking against NCERT Class 9–12 curriculum. Public results |
| Month 7–8 | Institutional partnerships — Gujarat education board, Pratham, Teach For India |
| Month 9–10 | 500 active users across 5 schools using government-distributed tablets |
| Month 11–12 | Open-source architecture release. Government EdTech grant applications |

---

## Running Locally

```bash
# Clone
git clone https://github.com/varunjarwani-max/alexander-os-v2
cd alexander-os-v2

# Install dependencies
pip install -r requirements.txt

# Pull models via Ollama
ollama pull gemma4:e2b
ollama pull qwen3:1.7b

# Start
python ui.py
# Open browser → localhost:5000
```

> Current prototype optimised for Apple Silicon via MLX. Android port using llama.cpp is in active development.

---

## The Vision

One year: 500 students across Gujarat government schools using Alexander OS on tablets they already own, with real accuracy data and one formal government or NGO partnership.

Wildest dream: Every student in a low-connectivity environment — rural India, Sub-Saharan Africa, Southeast Asia — has access to a tutor as capable as what a wealthy student gets in a city. The device is the equaliser. Alexander OS is the software that makes it real.

---

## Builder

**Varun Jarwani** — 18, Ahmedabad, India

Started coding at age 11. Ranked 10th globally in a coding competition at 13. Self-taught in Python, Java, HTML, CSS, and ML tooling. Built this prototype in 4 days during JEE preparation — the same pressure the students this is built for face every day.

No institutional backing. No funding. Just a laptop and the belief that where you're born should not determine what you get to learn.

---

## License

Apache 2.0 — open for anyone to use, build on, and improve.
