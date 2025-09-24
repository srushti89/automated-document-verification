import streamlit as st
import os
import json

from extract_text import extract_text

# Aadhaar
from verify_aadhaar import validate_text as validate_aadhaar_text, load_aadhaar_db, match_with_db as match_aadhaar_db

# PAN
from verify_pan import validate_text as validate_pan_text, load_pan_db, match_with_db as match_pan_db

# Driving License
from verify_dl import validate_text as validate_dl_text, load_dl_db, match_with_db as match_dl_db

st.set_page_config(page_title="Document Verification", layout="centered")

# ----------- PAGES -----------

def homepage():
    st.title("📄 Document Verification System")
    st.markdown("Welcome to the document verification portal.")
    st.markdown("Please select the type of document you want to verify and click **Next**.")

    doc_type = st.selectbox("Select Document Type", ["Aadhaar", "PAN", "Driving License"])
    st.session_state.selected_doc = doc_type

    if st.button("Next ➡️"):
        if doc_type == "Aadhaar":
            st.session_state.page = "aadhaar"
        elif doc_type == "PAN":
            st.session_state.page = "pan"
        elif doc_type == "Driving License":
            st.session_state.page = "dl"
        else:
            st.session_state.page = "coming_soon"

def aadhaar_page():
    st.title("🔍 Aadhaar Verification")
    uploaded_file = st.file_uploader("Upload Aadhaar Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img_path = save_image(uploaded_file)
        st.image(img_path, caption="📷 Uploaded Aadhaar", use_column_width=True)

        st.subheader("📄 Extracted Text")
        extracted = extract_text(img_path)
        st.code(extracted)

        st.subheader("✅ Aadhaar Validation")
        result = validate_aadhaar_text(extracted)
        st.json(result)

        if result["valid"]:
            st.subheader("🧾 Matching with Database")
            db = load_aadhaar_db()
            match_result = match_aadhaar_db(result, db)
            st.json(match_result)

            if match_result["matched"]:
                st.success("🎉 Aadhaar Verified Successfully!")
            else:
                st.warning("⚠️ Aadhaar Details Not Found in Database.")
        else:
            st.error("❌ Invalid Aadhaar")

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

def pan_page():
    st.title("🧾 PAN Card Verification")
    uploaded_file = st.file_uploader("Upload PAN Card Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img_path = save_image(uploaded_file)
        st.image(img_path, caption="📷 Uploaded PAN", use_column_width=True)

        st.subheader("📄 Extracted Text")
        extracted = extract_text(img_path)
        st.code(extracted)

        st.subheader("✅ PAN Validation")
        result = validate_pan_text(extracted)
        st.json(result)

        if result["valid"]:
            st.subheader("🧾 Matching with Database")
            db = load_pan_db()
            match_result = match_pan_db(result, db)
            st.json(match_result)

            if match_result["matched"]:
                st.success("🎉 PAN Verified Successfully!")
            else:
                st.warning("⚠️ PAN Details Not Found in Database.")
        else:
            st.error("❌ Invalid PAN Card")

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

def driving_license_page():
    st.title("🚘 Driving License Verification")
    uploaded_file = st.file_uploader("Upload Driving License Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img_path = save_image(uploaded_file)
        st.image(img_path, caption="📷 Uploaded License", use_column_width=True)

        st.subheader("📄 Extracted Text")
        extracted = extract_text(img_path)
        st.code(extracted)

        st.subheader("✅ DL Validation")
        result = validate_dl_text(extracted)
        st.json(result)

        if result["valid"]:
            st.subheader("🧾 Matching with Database")
            db = load_dl_db()
            match_result = match_dl_db(result, db)
            st.json(match_result)

            if match_result["matched"]:
                st.success("🎉 Driving License Verified Successfully!")
            else:
                st.warning("⚠️ License Details Not Found in Database.")
        else:
            st.error("❌ Invalid Driving License")

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

def coming_soon():
    st.title("🚧 Feature Coming Soon")
    doc_type = st.session_state.get("selected_doc", "Document")
    st.info(f"⚙️ {doc_type} verification is not implemented yet. Stay tuned!")

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

# ----------- Helpers -----------

def save_image(uploaded_file):
    os.makedirs("data", exist_ok=True)
    img_path = os.path.join("data", uploaded_file.name)
    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return img_path

# ----------- Navigation -----------

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    homepage()
elif st.session_state.page == "aadhaar":
    aadhaar_page()
elif st.session_state.page == "pan":
    pan_page()
elif st.session_state.page == "dl":
    driving_license_page()
elif st.session_state.page == "coming_soon":
    coming_soon()
