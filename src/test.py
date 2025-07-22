import streamlit as st
from PIL import Image

# Secure image display without using raw HTML embedding or base64
# Use Streamlit's built-in st.image to prevent XSS and avoid exposing file paths

def main():
    st.title("Secure Image Display")

    # Allow user to upload an image instead of reading arbitrary local files
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "gif"])
    if uploaded_file:
        try:
            # Read uploaded file as an Image object
            image = Image.open(uploaded_file)
            st.image(image, caption="User-uploaded image", use_column_width=True)
        except Exception as e:
            st.error(f"Failed to load image: {e}")

if __name__ == "__main__":
    main()
