import streamlit as st
import requests
from PIL import Image
import base64
import io

st.set_page_config(page_title="Smart Assistant - Image Classifier")

st.title("🧠 Smart Assistant")
st.subheader("Upload an image and get predictions from your AI model.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    if st.button("🔍 Predict"):
        with st.spinner("Querying model..."):
            res = requests.post("http://localhost:8000/predict", json={"image_base64": img_str})
            if res.status_code == 200:
                st.success(f"Prediction: {res.json()['prediction']}")
            else:
                st.error("Prediction failed. Check server logs.")
