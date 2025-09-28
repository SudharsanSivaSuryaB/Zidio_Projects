"""Captioning interface with extended captions."""
from typing import Optional
from PIL import Image

def generate_caption(image: Image.Image) -> str:
    """Generate a caption for the provided PIL Image with longer sentences."""
    try:
        from transformers import BlipProcessor, BlipForConditionalGeneration
        import torch
    except Exception:
        return "A descriptive placeholder caption for the uploaded image, illustrating its content in detail."

    try:
        processor = BlipProcessor.from_pretrained('Salesforce/blip-image-captioning-base')
        model = BlipForConditionalGeneration.from_pretrained('Salesforce/blip-image-captioning-base')
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model.to(device)

        if image.mode != 'RGB':
            image = image.convert('RGB')
        inputs = processor(images=image, return_tensors='pt').to(device)
        out = model.generate(**inputs, max_length=64, num_beams=5, repetition_penalty=1.2)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        return f"(Model error) Could not generate caption: {e}. You may need to download model weights."
