import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import pdf2image
import os
from io import BytesIO

st.set_page_config(page_title="📄 Document Converter & Organizer", layout="wide")

# Growth Mindset Challenge WebApp
st.title("🚀 Growth Mindset Challenge WebApp")
st.write("This project is created as part of Sir Zia's challenge, and I have implemented it in this way!")

# Title and Description
st.title("📄 All-in-One Document Converter & Organizer")
st.write("Easily convert images to PDFs, extract images from PDFs, merge multiple PDFs, or split a PDF into separate pages.")

# Feature Selection
option = st.radio("Select an option:", [
    "📷 Image to PDF", 
    "📄 PDF to Image", 
    "📑 Merge PDFs", 
    "✂️ Split PDF"
])

# Image to PDF Conversion
if option == "📷 Image to PDF":
    st.subheader("📷 Convert Images to a Single PDF")
    st.write("Upload multiple images (JPG or PNG), and merge them into a single PDF file.")
    uploaded_images = st.file_uploader("Upload Images", type=["jpg", "png"], accept_multiple_files=True)
    if uploaded_images:
        images = [Image.open(img).convert("RGB") for img in uploaded_images]
        if st.button("Convert to PDF"):
            pdf_buffer = BytesIO()
            images[0].save(pdf_buffer, save_all=True, append_images=images[1:])
            pdf_buffer.seek(0)
            st.download_button("Download PDF", pdf_buffer, "converted.pdf", "application/pdf")

# PDF to Image Conversion
elif option == "📄 PDF to Image":
    st.subheader("📄 Convert PDF to Images")
    st.write("Upload a PDF file and extract each page as an image (PNG format).")
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_pdf:
        images = pdf2image.convert_from_bytes(uploaded_pdf.read())
        for i, img in enumerate(images):
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            st.download_button(f"Download Page {i+1} as PNG", buffer, f"page_{i+1}.png", "image/png")

# Merge Multiple PDFs
elif option == "📑 Merge PDFs":
    st.subheader("📑 Merge Multiple PDFs into One")
    st.write("Upload multiple PDF files and combine them into a single document.")
    uploaded_pdfs = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
    if uploaded_pdfs and st.button("Merge PDFs"):
        merger = PdfWriter()
        for pdf in uploaded_pdfs:
            merger.append(PdfReader(pdf))
        merged_pdf = BytesIO()
        merger.write(merged_pdf)
        merged_pdf.seek(0)
        st.download_button("Download Merged PDF", merged_pdf, "merged.pdf", "application/pdf")

# Split a PDF into Multiple Pages
elif option == "✂️ Split PDF":
    st.subheader("✂️ Split PDF into Separate Pages")
    st.write("Upload a PDF and download each page as a separate file.")
    uploaded_pdf = st.file_uploader("Upload PDF to Split", type=["pdf"])
    if uploaded_pdf:
        reader = PdfReader(uploaded_pdf)
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            pdf_buffer = BytesIO()
            writer.write(pdf_buffer)
            pdf_buffer.seek(0)
            st.download_button(f"Download Page {i+1}", pdf_buffer, f"Page_{i+1}.pdf", "application/pdf")

# Footer 
st.markdown("---")
st.markdown("© 2025 All-in-One Document Converter & Organizer | Created by Fiza Asif")
