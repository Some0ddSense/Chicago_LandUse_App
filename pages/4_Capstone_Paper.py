import streamlit as st

# Use raw GitHub URL for reliable deployment
pdf_url = "https://raw.githubusercontent.com/some0ddsense/Chicago_LandUse_App/main/docs/Chicago_Land_Use_Explorer.pdf"

pdf_display = f"""
<embed
    src="{pdf_url}"
    type="application/pdf"
    width="100%"
    height="900px"
/>
"""

st.markdown(pdf_display, unsafe_allow_html=True)


