import os
import fitz  # PyMuPDF
from pdf2docx import Converter
try:
    from docx2pdf import convert as docx_to_pdf
except ImportError:
    docx_to_pdf = None

def convert_document(input_path, output_path, target_format):
    try:
        ext = os.path.splitext(input_path)[1].lower()
        target = target_format.lower()

        # 1. DOCX -> PDF
        if ext == '.docx' and target == 'pdf':
            if docx_to_pdf:
                # docx2pdf di Windows sangat reliabel (butuh MS Word)
                docx_to_pdf(input_path, output_path)
                return True
            return False

        # 2. PDF -> DOCX
        elif ext == '.pdf' and target == 'docx':
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            return True

        # 3. PDF -> JPG/PNG (Pakai PyMuPDF / fitz - Tidak butuh Poppler)
        elif ext == '.pdf' and (target == 'jpg' or target == 'png'):
            doc = fitz.open(input_path)
            page = doc.load_page(0)  # Ambil halaman pertama saja
            pix = page.get_pixmap()
            pix.save(output_path)
            doc.close()
            return True

        # 4. DOCX -> JPG (Convert to PDF first internally)
        elif ext == '.docx' and target == 'jpg':
            if not docx_to_pdf: return False
            
            temp_pdf = input_path.replace('.docx', '_temp.pdf')
            docx_to_pdf(input_path, temp_pdf)
            
            # Convert PDF temp to JPG
            doc = fitz.open(temp_pdf)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            pix.save(output_path)
            doc.close()
            
            # Cleanup
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)
            return True

        return False

    except Exception as e:
        print(f"[Document Error] {str(e)}")
        # Log error detail ke console/terminal
        return False