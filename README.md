---
title: AI Video Generator
emoji: 🎬
colorFrom: indigo
colorTo: purple
sdk: gradio
app_file: app.py
python_version: "3.12.12"
suggested_hardware: zero-a10g
pinned: false
---

# AI Video Generator

Production project source of truth.

## Runtime target

Gradio + Hugging Face ZeroGPU + Wan2.1 T2V 1.3B.

The model weights are downloaded from Hugging Face at runtime and are not stored in Git.

## Production certification gate

Certification requires all of the following:

1. GitHub CI green.
2. Hugging Face Space build succeeds.
3. Actual GPU runtime is confirmed from Space runtime/log evidence.
4. Wan model loads successfully.
5. A real text-to-video request completes.
6. A non-empty, valid MP4 is produced.
7. The generated video is returned to the Gradio player.
8. Failure/validation paths are exercised.
9. No unresolved deployment or runtime blocker remains.

A green GitHub workflow alone is not a production certificate.

## Source of truth

GitHub repository:
https://github.com/shehrozali6465372-ctrl/ai-video-generator

## Deployment policy

- Do not store model weights in Git.
- Keep secrets out of source control.
- Validate model/runtime compatibility before production deployment.
- Use a real end-to-end generation test before certification.
