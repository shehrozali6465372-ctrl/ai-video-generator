from __future__ import annotations


def validate_prompt(prompt: str) -> str:
    value = (prompt or "").strip()
    if not value:
        raise ValueError("Prompt is required.")
    if len(value) > 1000:
        raise ValueError("Prompt must be 1000 characters or fewer.")
    return value


def validate_generation_params(steps: int, frames: int, guidance: float) -> tuple[int, int, float]:
    steps = int(steps)
    frames = int(frames)
    guidance = float(guidance)
    if not 8 <= steps <= 40:
        raise ValueError("Inference steps must be between 8 and 40.")
    if frames not in {17, 25, 33, 41, 49}:
        raise ValueError("Frames must be one of 17, 25, 33, 41, or 49.")
    if not 1.0 <= guidance <= 12.0:
        raise ValueError("Guidance must be between 1 and 12.")
    return steps, frames, guidance
