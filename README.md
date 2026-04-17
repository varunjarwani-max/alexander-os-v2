# Alexander OS (v1.0-Prototype)
**High-Performance Offline AI Tutoring for K-12 on Entry-Level iPads**

Built during JEE/GSEB preparation to solve the accessibility gap in AI education. Alexander OS uses a dual-kernel architecture to provide multimodal (Vision/Audio) tutoring on devices with as little as 4GB of RAM.

### 🧠 The Architecture
- **Broker Kernel:** Gemma 4 E2B (2-bit quantized) for Trimodal Sensing (Vision/Audio/Text).
- **Specialist Kernel:** Qwen 3 (1.7B) for high-accuracy mathematical derivations.
- **Engine:** Memory-efficient "Cold-Swap" logic to prevent OOM (Out-of-Memory) crashes on iPad 10th/11th Gen hardware.

### 🛠️ Tech Stack
- **Backend:** Flask (Python-based Kernel Orchestrator)
- **Local Inference:** Ollama / MLX-LM
- **Hardware Target:** iPad A-series Neural Engine
