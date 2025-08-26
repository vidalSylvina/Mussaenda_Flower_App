import streamlit as st
from PIL import Image
import cv2
import numpy as np
from streamlit_drawable_canvas import st_canvas
import base64
from io import BytesIO

RHS_COLORS = [
    {"name": "RHS 43A", "code": "43A", "rgb": (209, 39, 52), "hex": "#D12734"},
    {"name": "RHS 43B", "code": "43B", "rgb": (232, 60, 69), "hex": "#E83C45"},
    {"name": "RHS 43C", "code": "43C", "rgb": (239, 87, 95), "hex": "#EF575F"},
    {"name": "RHS 43D", "code": "43D", "rgb": (253, 140, 138), "hex": "#FD8C8A"},
    {"name": "RHS 44A", "code": "44A", "rgb": (200, 38, 50), "hex": "#C82632"},
    {"name": "RHS 44B", "code": "44B", "rgb": (217, 28, 44), "hex": "#D91C2C"},
    {"name": "RHS 44C", "code": "44C", "rgb": (227, 69, 72), "hex": "#E34548"},
    {"name": "RHS 44D", "code": "44D", "rgb": (237, 97, 93), "hex": "#ED615D"},
    {"name": "RHS 45A", "code": "45A", "rgb": (173, 18, 47), "hex": "#AD122F"},
    {"name": "RHS 45B", "code": "45B", "rgb": (187, 0, 44), "hex": "#BB002C"},
    {"name": "RHS 45C", "code": "45C", "rgb": (202, 43, 68), "hex": "#CA2B44"},
    {"name": "RHS 45D", "code": "45D", "rgb": (208, 58, 82), "hex": "#D03A52"},
    {"name": "RHS N45A", "code": "N45A", "rgb": (158, 0, 39), "hex": "#9E0027"},
    {"name": "RHS N45B", "code": "N45B", "rgb": (171, 0, 47), "hex": "#AB002F"},
    {"name": "RHS N45C", "code": "N45C", "rgb": (183, 21, 59), "hex": "#B7153B"},
    {"name": "RHS N45D", "code": "N45D", "rgb": (196, 53, 80), "hex": "#C43550"},
    {"name": "RHS 46A", "code": "46A", "rgb": (150, 26, 50), "hex": "#961A32"},
    {"name": "RHS 46B", "code": "46B", "rgb": (179, 8, 52), "hex": "#B30834"},
    {"name": "RHS 46C", "code": "46C", "rgb": (205, 27, 67), "hex": "#CD1B43"},
    {"name": "RHS 46D", "code": "46D", "rgb": (215, 59, 86), "hex": "#D73B56"},
    {"name": "RHS 47A", "code": "47A", "rgb": (184, 52, 73), "hex": "#B83449"},
    {"name": "RHS 47B", "code": "47B", "rgb": (199, 49, 73), "hex": "#C73149"},
    {"name": "RHS 47C", "code": "47C", "rgb": (226, 83, 101), "hex": "#E25365"},
    {"name": "RHS 47D", "code": "47D", "rgb": (228, 100, 116), "hex": "#E46474"},
    {"name": "RHS 48A", "code": "48A", "rgb": (212, 95, 101), "hex": "#D45F65"},
    {"name": "RHS 48B", "code": "48B", "rgb": (227, 108, 117), "hex": "#E36C75"},
    {"name": "RHS 48C", "code": "48C", "rgb": (244, 127, 137), "hex": "#F47F89"},
    {"name": "RHS 48D", "code": "48D", "rgb": (255, 164, 170), "hex": "#FFA4AA"},
    {"name": "RHS 49A", "code": "49A", "rgb": (255, 152, 157), "hex": "#FF989D"},
    {"name": "RHS 49B", "code": "49B", "rgb": (253, 178, 171), "hex": "#FDB2AB"},
    {"name": "RHS 49C", "code": "49C", "rgb": (250, 203, 196), "hex": "#FACBC4"},
    {"name": "RHS 49D", "code": "49D", "rgb": (250, 218, 211), "hex": "#FADAD3"},
    {"name": "RHS 50A", "code": "50A", "rgb": (211, 44, 75), "hex": "#D32C4B"},
    {"name": "RHS 50B", "code": "50B", "rgb": (223, 81, 99), "hex": "#DF5163"},
    {"name": "RHS 50C", "code": "50C", "rgb": (235, 129, 140), "hex": "#EB818C"},
    {"name": "RHS 50D", "code": "50D", "rgb": (244, 191, 190), "hex": "#F4BFBE"},
    {"name": "RHS 51A", "code": "51A", "rgb": (208, 62, 95), "hex": "#D03E5F"},
    {"name": "RHS 51B", "code": "51B", "rgb": (218, 95, 116), "hex": "#DA5F74"},
    {"name": "RHS 51C", "code": "51C", "rgb": (223, 127, 138), "hex": "#DF7F8A"},
    {"name": "RHS 51D", "code": "51D", "rgb": (229, 158, 160), "hex": "#E59EA0"},
    {"name": "RHS 52A", "code": "52A", "rgb": (221, 60, 84), "hex": "#DD3C54"},
    {"name": "RHS 52B", "code": "52B", "rgb": (168, 64, 81), "hex": "#A84051"},
    {"name": "RHS 52C", "code": "52C", "rgb": (243, 116, 130), "hex": "#F37482"},
    {"name": "RHS 52D", "code": "52D", "rgb": (250, 149, 157), "hex": "#FA959D"}, 
    {"name": "RHS 53A", "code": "53A", "rgb": (146, 0, 51), "hex": "#920033"},
    {"name": "RHS 53B", "code": "53B", "rgb": (173, 33, 67), "hex": "#AD2143"},
    {"name": "RHS 53C", "code": "53C", "rgb": (193, 38, 67), "hex": "#C12643"},
    {"name": "RHS 53D", "code": "53D", "rgb": (204, 63, 98), "hex": "#CC3F62"},
    {"name": "RHS 178A", "code": "178A", "rgb": (128, 57, 59), "hex": "#80393B"},
    {"name": "RHS 178B", "code": "178B", "rgb": (142, 61, 62), "hex": "#8E3D3E"},
    {"name": "RHS 178C", "code": "178C", "rgb": (171, 74, 67), "hex": "#AB4A43"},
    {"name": "RHS 178D", "code": "178D", "rgb": (189, 87, 74), "hex": "#BD574A"},
    {"name": "RHS 179A", "code": "179A", "rgb": (171, 57, 63), "hex": "#AB393F"},
    {"name": "RHS 179B", "code": "179B", "rgb": (195, 88, 80), "hex": "#C35850"},
    {"name": "RHS 179C", "code": "179C", "rgb": (222, 135, 117), "hex": "#DE8775"},
    {"name": "RHS 179D", "code": "179D", "rgb": (240, 174, 150), "hex": "#F0AE96"},
    {"name": "RHS 180A", "code": "180A", "rgb": (161, 58, 67), "hex": "#A13A43"},
    {"name": "RHS 180B", "code": "180B", "rgb": (185, 76, 80), "hex": "#B94C50"},
    {"name": "RHS 180C", "code": "180C", "rgb": (195, 91, 95), "hex": "#C35B5F"},
    {"name": "RHS 180D", "code": "180D", "rgb": (205, 117, 116), "hex": "#CD7574"},
    {"name": "RHS 181A", "code": "181A", "rgb": (150, 58, 68), "hex": "#963A44"},
    {"name": "RHS 181B", "code": "181B", "rgb": (169, 74, 80), "hex": "#A94A50"},
    {"name": "RHS 181C", "code": "181C", "rgb": (184, 94, 101), "hex": "#B85E65"},
    {"name": "RHS 181D", "code": "181D", "rgb": (199, 131, 132), "hex": "#C78384"},
    {"name": "RHS 182A", "code": "182A", "rgb": (158, 61, 75), "hex": "#9E3D4B"},
    {"name": "RHS 182B", "code": "182B", "rgb": (163, 94, 96), "hex": "#A35E60"},
    {"name": "RHS 182C", "code": "182C", "rgb": (183, 121, 120), "hex": "#B77978"},
    {"name": "RHS 182D", "code": "182D", "rgb": (198, 129, 130), "hex": "#C68182"},
    {"name": "RHS 200A", "code": "200A", "rgb": (65, 47, 45), "hex": "#412F2D"},
    {"name": "RHS 200B", "code": "200B", "rgb": (81, 50, 46), "hex": "#51322E"},
    {"name": "RHS 200C", "code": "200C", "rgb": (94, 62, 52), "hex": "#5E3E34"},
    {"name": "RHS 200D", "code": "200D", "rgb": (112, 74, 56), "hex": "#704A38"},
    {"name": "RHS N200A", "code": "N200A", "rgb": (72, 57, 45), "hex": "#48392D"},
    {"name": "RHS N200B", "code": "N200B", "rgb": (108, 97, 90), "hex": "#6C615A"},
    {"name": "RHS N200C", "code": "N200C", "rgb": (149, 136, 133), "hex": "#958885"},
    {"name": "RHS N200D", "code": "N200D", "rgb": (182, 175, 172), "hex": "#B6AFAC"}, 
    {"name": "RHS 24A", "code": "24A", "rgb": (255, 155, 43), "hex": "#FF9B2B"},
    {"name": "RHS 24B", "code": "24B", "rgb": (255, 173, 80), "hex": "#FFAD50"},
    {"name": "RHS 24C", "code": "24C", "rgb": (255, 190, 127), "hex": "#FFBE7F"},
    {"name": "RHS 24D", "code": "24D", "rgb": (255, 202, 153), "hex": "#FFCA99"},
    {"name": "RHS 25A", "code": "25A", "rgb": (255, 136, 40), "hex": "#FF8828"},
    {"name": "RHS 25B", "code": "25B", "rgb": (255, 157, 60), "hex": "#FF9D3C"},
    {"name": "RHS 25C", "code": "25C", "rgb": (255, 169, 92), "hex": "#FFA95C"},
    {"name": "RHS 25D", "code": "25D", "rgb": (255, 196, 146), "hex": "#FFC492"},
    {"name": "RHS N25A", "code": "N25A", "rgb": (236, 103, 21), "hex": "#EC6715"},
    {"name": "RHS N25B", "code": "N25B", "rgb": (255, 129, 0), "hex": "#FF8100"},
    {"name": "RHS N25C", "code": "N25C", "rgb": (255, 143, 0), "hex": "#FF8F00"},
    {"name": "RHS N25D", "code": "N25D", "rgb": (255, 166, 0), "hex": "#FFA600"},
    {"name": "RHS 26A", "code": "26A", "rgb": (238, 136, 56), "hex": "#EE8838"},
    {"name": "RHS 26B", "code": "26B", "rgb": (247, 159, 85), "hex": "#F79F55"},
    {"name": "RHS 26C", "code": "26C", "rgb": (248, 177, 127), "hex": "#F8B17F"},
    {"name": "RHS 26D", "code": "26D", "rgb": (246, 188, 148), "hex": "#F6BC94"},
    {"name": "RHS 27A", "code": "27A", "rgb": (252, 209, 176), "hex": "#FCD1B0"},
    {"name": "RHS 27B", "code": "27B", "rgb": (255, 217, 193), "hex": "#FFD9C1"},
    {"name": "RHS 27C", "code": "27C", "rgb": (249, 221, 204), "hex": "#F9DDCC"},
    {"name": "RHS 27D", "code": "27D", "rgb": (248, 226, 207), "hex": "#F8E2CF"},
    {"name": "RHS 28A", "code": "28A", "rgb": (245, 106, 34), "hex": "#F56A22"},
    {"name": "RHS 28B", "code": "28B", "rgb": (255, 129, 48), "hex": "#FF8130"},
    {"name": "RHS 28C", "code": "28C", "rgb": (255, 167, 107), "hex": "#FFA76B"},
    {"name": "RHS 28D", "code": "28D", "rgb": (255, 183, 135), "hex": "#FFB787"},
    {"name": "RHS 29A", "code": "29A", "rgb": (255, 155, 96), "hex": "#FF9B60"},
    {"name": "RHS 29B", "code": "29B", "rgb": (255, 168, 121), "hex": "#FFA879"},
    {"name": "RHS 29C", "code": "29C", "rgb": (255, 193, 159), "hex": "#FFC19F"},
    {"name": "RHS 29D", "code": "29D", "rgb": (254, 213, 189), "hex": "#FED5BD"},
    {"name": "RHS 30A", "code": "30A", "rgb": (250, 109, 67), "hex": "#FA6D43"},
    {"name": "RHS 30B", "code": "30B", "rgb": (255, 115, 60), "hex": "#FF733C"},
    {"name": "RHS 30C", "code": "30C", "rgb": (255, 122, 60), "hex": "#FF7A3C"},
    {"name": "RHS 30D", "code": "30D", "rgb": (255, 137, 79), "hex": "#FF894F"},
    {"name": "RHS N30A", "code": "N30A", "rgb": (255, 48, 39), "hex": "#FF3027"},
    {"name": "RHS N30B", "code": "N30B", "rgb": (250, 83, 46), "hex": "#FA532E"},
    {"name": "RHS N30C", "code": "N30C", "rgb": (252, 98, 40), "hex": "#FC6228"},
    {"name": "RHS N30D", "code": "N30D", "rgb": (255, 114, 18), "hex": "#FF7212"},
    {"name": "RHS 31A", "code": "31A", "rgb": (234, 104, 63), "hex": "#EA683F"},
    {"name": "RHS 31B", "code": "31B", "rgb": (241, 122, 81), "hex": "#F17A51"},
    {"name": "RHS 31C", "code": "31C", "rgb": (236, 144, 114), "hex": "#EC9072"},
    {"name": "RHS 31D", "code": "31D", "rgb": (245, 162, 137), "hex": "#F5A289"},
    {"name": "RHS 32A", "code": "32A", "rgb": (243, 87, 57), "hex": "#F35739"},
    {"name": "RHS 32B", "code": "32B", "rgb": (253, 112, 71), "hex": "#FD7047"},
    {"name": "RHS 32C", "code": "32C", "rgb": (253, 137, 96), "hex": "#FD8960"},
    {"name": "RHS 32D", "code": "32D", "rgb": (255, 167, 136), "hex": "#FFA788"}, 
    {"name": "RHS 1A", "code": "1A", "rgb": (235, 224, 67), "hex": "#EBE043"},
    {"name": "RHS 1B", "code": "1B", "rgb": (232, 225, 87), "hex": "#E8E157"},
    {"name": "RHS 1C", "code": "1C", "rgb": (236, 232, 144), "hex": "#ECE890"},
    {"name": "RHS 1D", "code": "1D", "rgb": (241, 234, 164), "hex": "#F1EAA4"},
    {"name": "RHS 2A", "code": "2A", "rgb": (246, 225, 59), "hex": "#F6E13B"},
    {"name": "RHS 2B", "code": "2B", "rgb": (241, 227, 91), "hex": "#F1E35B"},
    {"name": "RHS 2C", "code": "2C", "rgb": (243, 236, 149), "hex": "#F3EC95"},
    {"name": "RHS 2D", "code": "2D", "rgb": (244, 234, 174), "hex": "#F4ECAE"},
    {"name": "RHS 3A", "code": "3A", "rgb": (250, 226, 64), "hex": "#FAE240"},
    {"name": "RHS 3B", "code": "3B", "rgb": (245, 228, 85), "hex": "#F5E455"},
    {"name": "RHS 3C", "code": "3C", "rgb": (246, 232, 128), "hex": "#F6E880"},
    {"name": "RHS 3D", "code": "3D", "rgb": (248, 237, 157), "hex": "#F8ED9D"},
    {"name": "RHS 4A", "code": "4A", "rgb": (248, 227, 93), "hex": "#F8E35D"},
    {"name": "RHS 4B", "code": "4B", "rgb": (247, 234, 125), "hex": "#F7EA7D"},
    {"name": "RHS 4C", "code": "4C", "rgb": (245, 233, 153), "hex": "#F5E999"},
    {"name": "RHS 4D", "code": "4D", "rgb": (245, 234, 191), "hex": "#F5EABF"},
    {"name": "RHS 5A", "code": "5A", "rgb": (247, 221, 191), "hex": "#F7DDBF"},
    {"name": "RHS 5B", "code": "5B", "rgb": (251, 226, 72), "hex": "#FBE248"},
    {"name": "RHS 5C", "code": "5C", "rgb": (249, 230, 115), "hex": "#F9E673"},
    {"name": "RHS 5D", "code": "5D", "rgb": (248, 231, 156), "hex": "#F8E79C"},
    {"name": "RHS 6A", "code": "6A", "rgb": (254, 221, 52), "hex": "#FEDD34"},
    {"name": "RHS 6B", "code": "6B", "rgb": (254, 223, 66), "hex": "#FEDF42"},
    {"name": "RHS 6C", "code": "6C", "rgb": (253, 224, 94), "hex": "#FDE05E"},
    {"name": "RHS 6D", "code": "6D", "rgb": (249, 228, 147), "hex": "#F9E493"},
    {"name": "RHS 7A", "code": "7A", "rgb": (246, 209, 39), "hex": "#F6D127"},
    {"name": "RHS 7B", "code": "7B", "rgb": (252, 218, 77), "hex": "#FCDA4D"},
    {"name": "RHS 7C", "code": "7C", "rgb": (254, 224, 83), "hex": "#FEE053"},
    {"name": "RHS 7D", "code": "7D", "rgb": (248, 228, 116), "hex": "#F8E474"},
    {"name": "RHS 8A", "code": "8A", "rgb": (254, 222, 88), "hex": "#FEDE58"},
    {"name": "RHS 8B", "code": "8B", "rgb": (254, 226, 116), "hex": "#FEE274"},
    {"name": "RHS 8C", "code": "8C", "rgb": (251, 229, 148), "hex": "#FBE594"},
    {"name": "RHS 8D", "code": "8D", "rgb": (245, 232, 186), "hex": "#F5E8BA"},
    {"name": "RHS 9A", "code": "9A", "rgb": (255, 217, 37), "hex": "#FFD925"},
    {"name": "RHS 9B", "code": "9B", "rgb": (255, 219, 62), "hex": "#FFDB3E"},
    {"name": "RHS 9C", "code": "9C", "rgb": (255, 225, 107), "hex": "#FFE16B"},
    {"name": "RHS 9D", "code": "9D", "rgb": (249, 229, 164), "hex": "#F9E5A4"}, 
    {"name": "RHS 10A", "code": "10A", "rgb": (253, 220, 107), "hex": "#FDDC6B"},
    {"name": "RHS 10B", "code": "10B", "rgb": (251, 223, 126), "hex": "#FBDF7E"}
    

]

def pil_to_base64(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return "data:image/png;base64," + base64.b64encode(byte_im).decode()

# Function for Light Correction 
def correct_lighting(image): 
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    #Apply CLAHE (adaptive histogram equalization) to L channel
    #Contrast Limited Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l_corrected = clahe.apply(l)
    
    lab = cv2.merge((l_corrected, a, b))
    corrected_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return corrected_image


# Function for displaying original image
def original_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")            # Open image with PIL and convert to RGB
    image = np.array(image)                                     # Convert PIL Image to NumPy array                             
    image = cv2.resize(image, (800, 800))                       # Resize image
    return image

# Function to preprocess the uploaded image
def preprocess_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")            # Open image with PIL and convert to RGB
    image = np.array(image)                                     # Convert PIL Image to NumPy array                             
    image = cv2.resize(image, (800, 800))                       # Resize image
    image = correct_lighting(image) #addes lighting corrector
    return image

# Function to find closest RHS color using simple RGB distance
def find_closest_rhs_color(rgb):
    min_distance = float('inf')
    closest_color = None
    for rhs in RHS_COLORS:
        rhs_rgb = np.array(rhs["rgb"])
        clicked_rgb_arr = np.array(rgb)
        dist = np.linalg.norm(rhs_rgb - clicked_rgb_arr)
        if dist < min_distance:
            min_distance = dist
            closest_color = rhs
    return closest_color

def display_color_swatch(color_hex, label, size=50):
    swatch_html = f"""
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
        <div style="
            width: {size}px;
            height: {size}px;
            background-color: {color_hex};
            border: 1px solid #000;
            border-radius: 5px;
            margin-right: 10px;
        "></div>
        <div style="font-size: 16px;">{label}</div>
    </div>
    """
    st.markdown(swatch_html, unsafe_allow_html=True)


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
    orig_image = original_image(images_uploaded)
    preprocessed = preprocess_image(images_uploaded)
    
    orig_pil_image = Image.fromarray(orig_image)
    pil_image = Image.fromarray(preprocessed)           # Convert to PIL image for canvas
   

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Original Photo")
        st.image(orig_pil_image, caption="Original Image", width=800)

        
        st.subheader("Click on the Image") 
        # Display drawable canvas (Interactive) 
        canvas_res = st_canvas(
            fill_color="rgba(0, 255, 0, 0.3)",
            stroke_width=2,
            stroke_color="black",
            background_color=None,
            background_image=pil_image,  # ✅ pass PIL Image
            update_streamlit=True,
            height=orig_pil_image.height,
            width=orig_pil_image.width,
            drawing_mode="point",
            point_display_radius=5,
            key="canvas"
        )

    
        # if user clicked on image 
        if canvas_res.json_data is not None and len(canvas_res.json_data["objects"]) > 0: 
            # Get the last clicked point 
            last_object = canvas_res.json_data["objects"][-1]
            x = int(last_object["left"])
            y = int(last_object["top"])
            
            if 0 <= x < pil_image.width and 0 <= y < pil_image.height:
                clicked_rgb = pil_image.getpixel((x, y))
                clicked_hex = '#%02x%02x%02x' % clicked_rgb
        
                # Get RGB from image at clicked position
                clicked_rgb = pil_image.getpixel((x, y))
                st.markdown(f"### Clicked Coordinates: ({x}, {y})")
                st.markdown(f"### RGB Value: {clicked_rgb}")
                display_color_swatch(clicked_hex, "")
                
                # Find closest RHS color
                match = find_closest_rhs_color(clicked_rgb)

                if match:
                    st.success(f"## ✅ Closest RHS Color: **{match['name']}** ({match['code']})")
                    display_color_swatch(match["hex"], f"")

        

