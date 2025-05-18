import streamlit as st
from PIL import Image
from stego_utils import hide_message_in_image, extract_message_from_image
from streamlit_option_menu import option_menu
import io

# Konfigurasi halaman
st.set_page_config(page_title="Steganografi Forensik", layout="wide")

# Sidebar
with st.sidebar:
    #st.image("logo.png", use_column_width=True)
    selected = option_menu(
        menu_title=None,
        options=["Sisipkan Pesan", "Ekstrak Pesan"],
        icons=["shield-lock", "search"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#f8f9fa", "color": "#0E1117"},
            "icon": {"color": "#0E1117", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#DBD3D3",
                "color": "#0E1117"
            },
            "nav-link-selected": {"background-color": "#0f0f43", "color": "#f8f9fa"},
        }
    )

st.title("🕵️‍♂️ Aplikasi Steganografi Forensik")

# =============================
# Menu: Sisipkan Pesan
# =============================
if selected == "Sisipkan Pesan":
    st.header("🔐 Sisipkan Pesan ke dalam Gambar")
    uploaded_image = st.file_uploader("Unggah Gambar (PNG/JPG)", type=["png", "jpg", "jpeg"])
    secret_message = st.text_area("Masukkan Pesan Rahasia")

    if uploaded_image and secret_message:
        image = Image.open(uploaded_image)

        if st.button("Sisipkan Pesan"):
            try:
                encoded_img = hide_message_in_image(image, secret_message)
                st.success("✅ Pesan berhasil disisipkan!")
                st.image(encoded_img, caption="Gambar dengan Pesan", use_column_width=True)

                # Download button
                buf = io.BytesIO()
                encoded_img.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button("📥 Unduh Gambar", data=byte_im, file_name="encoded_image.png", mime="image/png")
            except ValueError as e:
                st.error(f"❌ {str(e)}")

# =============================
# Menu: Ekstrak Pesan
# =============================
elif selected == "Ekstrak Pesan":
    st.header("🔍 Ekstrak Pesan dari Gambar")
    uploaded_image = st.file_uploader("Unggah Gambar", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)

        if st.button("Ekstrak Pesan"):
            with st.spinner("Mengekstrak..."):
                message = extract_message_from_image(image)
            st.success("✅ Ekstraksi selesai!")
            st.text_area("Pesan Tersembunyi", value=message, height=200)
