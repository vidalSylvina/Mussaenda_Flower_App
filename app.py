import streamlit as st
from PIL import Image
import cv2
import numpy as np
from streamlit_drawable_canvas import st_canvas

RHS_COLORS = [
    {"name": "RHS 46A", "code": "46A", "rgb": (204, 0, 0), "hex": "#cc0000"},
    {"name": "RHS 53B", "code": "53B", "rgb": (255, 51, 51), "hex": "#ff3333"},
    {"name": "RHS 61B", "code": "61B", "rgb": (255, 102, 102), "hex": "#ff6666"},
    {"name": "RHS 70B", "code": "70B", "rgb": (255, 204, 204), "hex": "#ffcccc"},
    {"name": "RHS 155C", "code": "155C", "rgb": (255, 255, 240), "hex": "#fffff0"},
    {"name": "RHS N155B", "code": "N155B", "rgb": (255, 255, 255), "hex": "#ffffff"}
]


# Function to preprocess the uploaded image
def preprocess_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")            # Open image with PIL and convert to RGB
    image = np.array(image)                                     # Convert PIL Image to NumPy array                             
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)              # Convert RGB to BGR color space 
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
    #resized image
    preprocessed = preprocess_image(images_uploaded)
    
    #image_rgb = cv2.cvtColor(preprocessed, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(preprocessed)           # Convert to PIL image for canvas
   

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Original Photo")
        st.image(pil_image, caption="Original Image", width=800)

        
        st.subheader("Click on the Image") 
        # Display drawable canvas (Interactive) 
        canvas_res = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # translucent fill color
            stroke_width=1,
            background_image=pil_image,
            update_streamlit=True,
            height=800,
            width=800,
            drawing_mode="point",
            key="canvas",
            background_color=None
        )
    
        # if user clicked on image 
        if canvas_res.json_data is not None and len(canvas_res.json_data["objects"]) > 0: 
            # Get the last clicked point 
            last_object = canvas_res.json_data["objects"][-1]
            x = int(last_object["left"])
            y = int(last_object["top"])
        
            # Get RGB from image at clicked position
            clicked_rgb = pil_image.getpixel((x, y))
            st.success(f"Clicked Coordinates: ({x}, {y})")
            st.info(f"RGB Value: {clicked_rgb}")

        

