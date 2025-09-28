import streamlit as st
from PIL import Image
import numpy as np

from src.captioning.blip_captioner import generate_caption
from src.segmentation.segmenter import predict_boxes, draw_boxes

st.set_page_config(page_title='Image Captioning + YOLOv8 Detection', layout='centered')
st.title('Image Captioning + YOLOv8 Object Detection — Demo')

st.markdown('Upload an image, generate a caption, and highlight objects with bounding boxes (YOLOv8, >600 classes).')

uploaded = st.file_uploader('Upload an image', type=['png','jpg','jpeg'])
run_caption = st.button('Generate Caption')
run_segment = st.button('Run Object Detection')

if uploaded is not None:
    image = Image.open(uploaded).convert('RGB')
    st.image(image, caption='Input image', use_column_width=True)

    if run_caption:
        with st.spinner('Generating caption...'):
            caption = generate_caption(image)
        st.success('Generated Caption:')
        st.write(caption)

    if run_segment:
        with st.spinner('Detecting objects (YOLOv8)...'):
            boxes = predict_boxes(image, conf=0.25)
            boxed_img = draw_boxes(np.array(image), boxes)
        st.image(boxed_img, caption='Objects highlighted with bounding boxes', use_column_width=True)
else:
    st.info('Upload an image to get started.')
