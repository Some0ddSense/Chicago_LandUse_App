import streamlit as st

# Use raw GitHub URL for reliable deployment
pdf_url = "https://raw.githubusercontent.com/some0ddsense/Chicago_LandUse_App/main/docs/Chicago_Land_Use_Explorer.pdf"

pdf_display = f"""
<iframe
    src="{pdf_url}"
    width="100%"
    height="900px"
    style="border: none;">
</iframe>
<p><a href="{pdf_url}" target="_blank">Open PDF in new tab</a></p>
"""

st.markdown(pdf_display, unsafe_allow_html=True)


