---
title: AI Video Generator
emoji: 🎬
colorFrom: indigo
colorTo: purple
sdk: static
pinned: false
---

# AI Video Generator

Production project source of truth.

## Current deployment phase

The project is currently prepared as a free Static Space while requesting Hugging Face GPU/ZeroGPU access.

The runtime target is a Gradio + ZeroGPU video-generation backend. Model selection and inference configuration will be locked only after compatibility and runtime verification.

## Source of truth

GitHub repository:
https://github.com/shehrozali6465372-ctrl/ai-video-generator

## Deployment policy

- Do not store model weights in Git.
- Keep secrets out of source control.
- Validate model/runtime compatibility before production deployment.
- Production certification requires a real end-to-end generation test and runtime log evidence.
