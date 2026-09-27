import os
import tempfile
import uuid
from pathlib import Path
from threading import Lock

import spaces
import gradio as gr
import torch
from diffusers import WanPipeline
from diffusers.utils import export_to_video

from validation import validate_generation_params, validate_prompt

MODEL_ID = os.getenv("MODEL_ID", "Wan-AI/Wan2.1-T2V-1.3B-Diffusers")
OUTPUT_DIR = Path(tempfile.gettempdir()) / "ai-video-generator"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
GENERATION_LOCK = Lock()
MAX_OUTPUT_FILES = 4

if not torch.cuda.is_available():
    raise RuntimeError("This application requires a ZeroGPU/accelerated runtime.")

pipe = WanPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16)
pipe.to("cuda")


@spaces.GPU(duration=120)
def generate_video(prompt: str, steps: int, frames: int, guidance: float):
    try:
        prompt = validate_prompt(prompt)
        steps, frames, guidance = validate_generation_params(steps, frames, guidance)
    except ValueError as exc:
        raise gr.Error(str(exc)) from exc

    output = OUTPUT_DIR / f"{uuid.uuid4().hex}.mp4"
    try:
        with GENERATION_LOCK:
            result = pipe(
                prompt=prompt,
                num_inference_steps=steps,
                num_frames=frames,
                guidance_scale=guidance,
            )
            export_to_video(result.frames[0], str(output), fps=16)
        if not output.is_file() or output.stat().st_size == 0:
            raise RuntimeError("Video generation completed without a valid MP4 output.")
        _cleanup_old_outputs()
        return str(output)
    except gr.Error:
        raise
    except Exception as exc:
        raise gr.Error("Video generation failed. Please retry with a shorter prompt.") from exc


def _cleanup_old_outputs() -> None:
    outputs = sorted(
        OUTPUT_DIR.glob("*.mp4"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for stale in outputs[MAX_OUTPUT_FILES:]:
        try:
            stale.unlink()
        except OSError:
            pass


with gr.Blocks(title="AI Video Generator") as demo:
    gr.Markdown("# AI Video Generator")
    gr.Markdown("Generate a short text-to-video clip with Wan2.1 T2V 1.3B.")
    prompt = gr.Textbox(
        label="Prompt",
        placeholder="A cinematic shot of a futuristic city at sunset...",
        lines=4,
        max_lines=8,
    )
    with gr.Row():
        steps = gr.Slider(8, 40, value=20, step=1, label="Inference steps")
        frames = gr.Dropdown(choices=[17, 25, 33, 41, 49], value=25, label="Frames")
        guidance = gr.Slider(1, 12, value=6, step=0.5, label="Guidance")
    generate = gr.Button("Generate video", variant="primary")
    output = gr.Video(label="Generated video")
    generate.click(fn=generate_video, inputs=[prompt, steps, frames, guidance], outputs=output)

if __name__ == "__main__":
    demo.queue(max_size=4).launch()
