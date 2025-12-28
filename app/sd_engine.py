from diffusers import StableDiffusionPipeline
import torch

MODEL_NAME = "runwayml/stable-diffusion-v1-5"

print("Loading Stable Diffusion… please wait 20–40 seconds…")

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

if torch.cuda.is_available():
    pipe = pipe.to("cuda")


def generate_ai_image(prompt: str):
    # Automatically enhance the prompt for meme-style images
    meme_prompt = (
        f"{prompt}, meme template style, reaction image, bold facial expression,clean background, high contrast, centered subject, humorous tone,image should make sense,text should not be more than 3 words"
    )

    print("Generating meme-style image with prompt:", meme_prompt)

    # Generate image using the Turbo model
    image = pipe(
        meme_prompt,
        num_inference_steps=50,
        guidance_scale=0.0
    ).images[0]

    return image

