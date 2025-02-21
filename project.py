import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import pdf2image
import shutil
import os
from io import BytesIO

st.set_page_config(page_title="📄 Document Converter & Organizer", layout="wide")

# Poppler Check (Required for PDF to Image conversion)
if not shutil.which("pdftoppm"):
    st.error("Error: Poppler is not installed. Please add `poppler-utils` to `packages.txt` and redeploy.")
    st.stop()

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
        images = []
        for img in uploaded_images:
            try:
                image = Image.open(img).convert("RGB")
                images.append(image)
            except Exception as e:
                st.error(f"Error processing image: {e}")
        
        if images and st.button("Convert to PDF"):
            pdf_buffer = BytesIO()
            if len(images) > 1:
                images[0].save(pdf_buffer, save_all=True, append_images=images[1:])
            else:
                images[0].save(pdf_buffer, format="PDF")
            pdf_buffer.seek(0)
            st.download_button("Download PDF", pdf_buffer, "converted.pdf", "application/pdf")

# PDF to Image Conversion
elif option == "📄 PDF to Image":
    st.subheader("📄 Convert PDF to Images")
    st.write("Upload a PDF file and extract each page as an image (PNG format).")

    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_pdf:
        try:
            images = pdf2image.convert_from_bytes(uploaded_pdf.read())
            for i, img in enumerate(images):
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)
                st.download_button(f"Download Page {i+1} as PNG", buffer, f"page_{i+1}.png", "image/png")
        except Exception as e:
            st.error(f"Error processing PDF: {e}")

# Merge Multiple PDFs
elif option == "📑 Merge PDFs":
    st.subheader("📑 Merge Multiple PDFs into One")
    st.write("Upload multiple PDF files and combine them into a single document.")

    uploaded_pdfs = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

    if uploaded_pdfs and st.button("Merge PDFs"):
        merger = PdfWriter()
        for pdf in uploaded_pdfs:
            try:
                merger.append(PdfReader(pdf))
            except Exception as e:
                st.error(f"Error merging PDF: {e}")

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
        try:
            reader = PdfReader(uploaded_pdf)
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                pdf_buffer = BytesIO()
                writer.write(pdf_buffer)
                pdf_buffer.seek(0)
                st.download_button(f"Download Page {i+1}", pdf_buffer, f"Page_{i+1}.pdf", "application/pdf")
        except Exception as e:
            st.error(f"Error processing PDF: {e}")

# Footer 
st.markdown("---")
st.markdown("© 2025 All-in-One Document Converter & Organizer | Created by Fiza")
