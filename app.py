import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
from PIL import Image
import io

# --- Helper to process images for PDF ---
def process_image(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Convert to RGB if necessary (to handle PNG transparency)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        return img_byte_arr
    return None

def generate_pdf(data, photo_bytes):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, "Faculty Performance Report", ln=True, align='C')
    pdf.ln(10)

    # Sidebar/Photo Logic
    if photo_bytes:
        # Save temp image for FPDF to grab
        with open("temp_photo.jpg", "wb") as f:
            f.write(photo_bytes.getbuffer())
        pdf.image("temp_photo.jpg", x=150, y=30, w=40)

    # Faculty Info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, "Name: ", 0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, data['name'], ln=True)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, "Faculty ID: ", 0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, data['id'], ln=True)
    
    pdf.ln(20) # Space after header/photo

    # Workload Section
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, " Academic Workload", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, f"Subjects: {', '.join(data['subjects'])}")
    pdf.multi_cell(0, 10, f"Labs: {', '.join(data['labs'])}")

    # Publications
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, " Research & Publications", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    for paper in data['papers']:
        pdf.cell(0, 10, f"- {paper}", ln=True)

    # Score
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(39, 174, 96) # Green color for score
    pdf.cell(0, 10, f"Final Performance Score: {data['score']}", ln=True, align='C')

    return pdf.output(dest='S').encode('latin-1')

# --- Streamlit UI ---
st.title("Faculty ERP with Photo Report")

with st.form("erp_form"):
    col1, col2 = st.columns([1, 2])
    with col1:
        photo = st.file_uploader("Upload Profile Photo", type=['jpg', 'jpeg', 'png'])
    with col2:
        name = st.text_input("Full Name")
        f_id = st.text_input("Faculty ID")

    subjects = st.multiselect("Subjects", ["AI", "Math", "Physics", "CS"])
    labs = st.multiselect("Labs", ["Hardware Lab", "Software Lab"])
    papers = st.text_area("Research Paper Titles (One per line)")
    
    submitted = st.form_submit_button("Generate Report")

if submitted:
    paper_list = [p.strip() for p in papers.split('\n') if p.strip()]
    score = (len(subjects) * 10) + (len(labs) * 15) + (len(paper_list) * 50)
    
    faculty_data = {
        "name": name, "id": f_id, "subjects": subjects, 
        "labs": labs, "papers": paper_list, "score": score
    }

    photo_processed = process_image(photo)
    pdf_output = generate_pdf(faculty_data, photo_processed)

    st.success(f"Score Calculated: {score}")
    st.download_button("Download PDF Report", data=pdf_output, file_name="Faculty_Report.pdf")
