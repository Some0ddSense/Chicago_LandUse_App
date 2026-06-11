import streamlit as st
import base64

pdf_path = "docs/Chicago_Land_Use_Explorer.pdf"

with open(pdf_path, "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode("utf-8")

pdf_display = f"""
<embed
    src="data:application/pdf;base64,{base64_pdf}"
    type="application/pdf"
    width="100%"
    height="800"
/>
"""

st.markdown(pdf_display, unsafe_allow_html=True)

