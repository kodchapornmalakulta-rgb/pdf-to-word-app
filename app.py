import streamlit as st
from pdf2docx import Converter
import tempfile
import os

# ตกแต่งหน้าเว็บ
st.set_page_config(page_title="PDF to Word Converter", page_icon="📝")
st.title("ระบบแปลงไฟล์ PDF เป็น Word 📄➡️📝")
st.write("ยินดีต้อนรับค่ะ! กรุณาอัปโหลดไฟล์ PDF ที่ต้องการแปลงเป็นเอกสาร Word")

# สร้างกล่องสำหรับอัปโหลดไฟล์
uploaded_file = st.file_uploader("ลากไฟล์มาวาง หรือคลิกเพื่อเลือกไฟล์ PDF", type="pdf")

if uploaded_file is not None:
    st.info(f"เตรียมแปลงไฟล์: {uploaded_file.name}")
    
    # สร้างปุ่มกดเพื่อเริ่มทำงาน
    if st.button("🚀 เริ่มแปลงไฟล์"):
        with st.spinner("กำลังประมวลผล กรุณารอสักครู่..."):
            
            # จำลองพื้นที่เก็บไฟล์ชั่วคราว
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(uploaded_file.getvalue())
                pdf_path = tmp_pdf.name
            
            docx_path = pdf_path.replace(".pdf", ".docx")
            
            try:
                # เริ่มกระบวนการแปลงไฟล์เหมือนใน Colab
                cv = Converter(pdf_path)
                cv.convert(docx_path)
                cv.close()
                
                # เตรียมไฟล์สำหรับให้ดาวน์โหลด
                with open(docx_path, "rb") as docx_file:
                    st.success("🎉 แปลงไฟล์เสร็จสมบูรณ์แล้วค่ะ!")
                    st.download_button(
                        label="⬇️ คลิกที่นี่เพื่อดาวน์โหลดไฟล์ Word",
                        data=docx_file,
                        file_name=uploaded_file.name.replace(".pdf", ".docx"),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            except Exception as e:
                st.error(f"ขออภัยค่ะ เกิดข้อผิดพลาด: {e}")
            finally:
                # ลบไฟล์ชั่วคราวทิ้งเพื่อไม่ให้รกเซิร์ฟเวอร์
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
                if os.path.exists(docx_path):
                    os.remove(docx_path)
