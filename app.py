import streamlit as st
from PIL import Image
import cv2
import numpy as np

# Function to preprocess the uploaded image
def preprocess_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")            # Open image with PIL and convert to RGB
    image = np.array(image)                                     # Convert PIL Image to NumPy array                             
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)              # Convert RGB to BGR color space 
    image = cv2.resize(image, (800, 800))                       # Resize image
    return image

# title and layout
st.set_page_config(page_title="Mussaenda Flower Color Identifier", layout="wide")

# Apply CSS styles
st.markdown(
    """
    <style>
    .stApp {
        background-color: #e6f2ff;
    }
    h1 {
        text-align: center;
        color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display centered page title
st.markdown("<h1>Mussaenda Flower Color Identifier 🌸</h1>", unsafe_allow_html=True)

# File uploader widget that accepts image files
images_uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# If an image is uploaded
if images_uploaded is not None:
    preprocessed = preprocess_image(images_uploaded)
    image_rgb = cv2.cvtColor(preprocessed, cv2.COLOR_BGR2RGB)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image_rgb, caption="Preprocessed Image", channels="RGB", use_container_width=True)
