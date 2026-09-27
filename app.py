import os
import tempfile
import uuid
from pathlib import Path

import gradio as gr
import spaces
import torch
from diffusers import WanPipeline
from diffusers.utils import export_to_video

MODEL_ID = os.getenv("MODEL_ID", "Wan-AI/Wan2.1-T2V-1.3B-Diffusers")
OUTPUT_DIR = Path(tempfile.gettempdir()) / "ai-video-generator"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not torch.cuda.is_available():
    raise RuntimeError("This application requires a ZeroGPU/accelerated runtime.")

pipe = WanPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16,
)
pipe.to("cuda")


def validate_prompt(prompt: str) -> str:
    prompt = (prompt or "").strip()
    if not prompt:
        raise gr.Error("Prompt is required.")
    if len(prompt) > 1000:
        raise gr.Error("Prompt must be 1000 characters or fewer.")
    return prompt


@spaces.GPU(duration=120)
def generate_video(prompt: str, steps: int, frames: int, guidance: float):
    prompt = validate_prompt(prompt)
    steps = int(steps)
    frames = int(frames)
    guidance = float(guidance)

    if not 8 <= steps <= 40:
        raise gr.Error("Inference steps must be between 8 and 40.")
    if frames not in {17, 25, 33, 41, 49}:
        raise gr.Error("Frames must be one of 17, 25, 33, 41, or 49.")
    if not 1.0 <= guidance <= 12.0:
        raise gr.Error("Guidance must be between 1 and 12.")

    result = pipe(
        prompt=prompt,
        num_inference_steps=steps,
        num_frames=frames,
        guidance_scale=guidance,
    )

    output = OUTPUT_DIR / f"{uuid.uuid4().hex}.mp4"
    export_to_video(result.frames[0], str(output), fps=8)
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError("Video generation completed without a valid MP4 output.")
    return str(output)


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
        frames = gr.Dropdown(
            choices=[17, 25, 33, 41, 49],
            value=25,
            label="Frames",
        )
        guidance = gr.Slider(1, 12, value=6, step=0.5, label="Guidance")
    generate = gr.Button("Generate video", variant="primary")
    output = gr.Video(label="Generated video")
    generate.click(
        fn=generate_video,
        inputs=[prompt, steps, frames, guidance],
        outputs=output,
    )

if __name__ == "__main__":
    demo.queue(max_size=4).launch()
