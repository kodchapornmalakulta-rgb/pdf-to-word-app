import streamlit as st
from pdf2docx import Converter
import fitz  # PyMuPDF สำหรับแปลงเป็นรูปภาพ
import tempfile
import os
import zipfile
import io

# ตกแต่งหน้าเว็บ
st.set_page_config(page_title="PDF Converter All-in-One", page_icon="📝")
st.title("ระบบแปลงไฟล์ PDF ครบวงจร 📄✨")
st.write("ยินดีต้อนรับค่ะคุณครู! สามารถเลือกแปลงไฟล์ PDF เป็น Word หรือ รูปภาพได้ที่นี่เลยค่ะ")

# สร้างปุ่มเลือกโหมดการทำงาน
mode = st.radio(
    "เลือกรูปแบบผลลัพธ์ที่ต้องการ:",
    ["📝 แปลงเป็นไฟล์ Word (.docx)", "🖼️ แปลงเป็นรูปภาพ (.png)"]
)

# สร้างกล่องสำหรับอัปโหลดไฟล์
uploaded_file = st.file_uploader("ลากไฟล์มาวาง หรือคลิกเพื่อเลือกไฟล์ PDF", type="pdf")

if uploaded_file is not None:
    st.info(f"ไฟล์ที่เลือก: {uploaded_file.name}")
    
    # สร้างปุ่มกดเพื่อเริ่มทำงาน
    if st.button("🚀 เริ่มแปลงไฟล์"):
        with st.spinner("กำลังประมวลผล กรุณารอสักครู่..."):
            
            # จำลองพื้นที่เก็บไฟล์ชั่วคราว
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(uploaded_file.getvalue())
                pdf_path = tmp_pdf.name
            
            try:
                if "Word" in mode:
                    # โหมดแปลงเป็น Word
                    docx_path = pdf_path.replace(".pdf", ".docx")
                    cv = Converter(pdf_path)
                    cv.convert(docx_path)
                    cv.close()
                    
                    with open(docx_path, "rb") as docx_file:
                        st.success("🎉 แปลงไฟล์เป็น Word เสร็จสมบูรณ์แล้วค่ะ!")
                        st.download_button(
                            label="⬇️ คลิกที่นี่เพื่อดาวน์โหลดไฟล์ Word",
                            data=docx_file,
                            file_name=uploaded_file.name.replace(".pdf", ".docx"),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    if os.path.exists(docx_path):
                        os.remove(docx_path)
                        
                else:
                    # โหมดแปลงเป็นรูปภาพ
                    doc = fitz.open(pdf_path)
                    zip_buffer = io.BytesIO()
                    
                    # รวบรวมรูปภาพทุกหน้าใส่ในไฟล์ ZIP
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                        for page_num in range(len(doc)):
                            page = doc.load_page(page_num)
                            pix = page.get_pixmap(dpi=150)  # ความละเอียดคมชัดกำลังดี
                            img_data = pix.tobytes("png")
                            
                            img_name = f"page_{page_num + 1}.png"
                            zip_file.writestr(img_name, img_data)
                            
                    st.success("🎉 แปลงไฟล์เป็นรูปภาพเสร็จสมบูรณ์แล้วค่ะ! (รวมทุกหน้าไว้ในไฟล์ ZIP เรียบร้อย)")
                    st.download_button(
                        label="⬇️ คลิกที่นี่เพื่อดาวน์โหลดรูปภาพทั้งหมด (ไฟล์ .zip)",
                        data=zip_buffer.getvalue(),
                        file_name=uploaded_file.name.replace(".pdf", "_images.zip"),
                        mime="application/zip"
                    )
                    
            except Exception as e:
                st.error(f"ขออภัยค่ะ เกิดข้อผิดพลาด: {e}")
            finally:
                # ลบไฟล์ชั่วคราวทิ้ง
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
