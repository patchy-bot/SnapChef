import streamlit as st
import bleach

# Securely render user-provided HTML by sanitizing with bleach

# Define allowed HTML tags and attributes
ALLOWED_TAGS = [
    'b', 'i', 'u', 'em', 'strong', 'a', 'p', 'ul', 'ol', 'li', 'br'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel'],
}


def main():
    st.title("Secure Content Renderer")

    uploaded = st.file_uploader("Upload HTML or Markdown file", type=["html", "md"])
    if uploaded:
        raw_content = uploaded.read().decode('utf-8', errors='replace')
        # Sanitize HTML
        clean_content = bleach.clean(
            raw_content,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True
        )
        # Render sanitized content; unsafe_allow_html=True is safe now after bleach sanitization
        st.markdown(clean_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
