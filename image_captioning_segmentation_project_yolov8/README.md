# Image Captioning & Segmentation

This project is a minimal, well-structured starter implementation for the Image Captioning + Segmentation project.
It follows the supplied project document: provides captioning (BLIP-compatible), segmentation (UNet placeholder),
visualization utilities, and a Streamlit demo for local testing.

## Structure
- `app/streamlit_app.py` - Streamlit demo app (upload image, run captioning & segmentation).
- `src/captioning/blip_captioner.py` - Captioning interface (tries to use HuggingFace BLIP; falls back to a stub).
- `src/segmentation/segmenter.py` - Segmentation interface (UNet class + predict wrapper; falls back to simple edge-based mask).
- `src/common/viz.py` - Visualization helpers (overlay mask on image).
- `notebooks/` - starter Jupyter notebook templates.
- `requirements.txt` - Python packages to install.

## Quick start (local)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Notes:
- The repo is written defensively: if large pretrained models aren't available the app will still run and produce safe placeholder outputs.
- For production usage, follow the comments in the modules to download appropriate weights (BLIP / trained UNet or Mask-RCNN).
