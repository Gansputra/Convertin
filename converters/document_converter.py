import os
import fitz 
from pdf2docx import Converter
try:
    from docx2pdf import convert as docx_to_pdf
except ImportError:
    docx_to_pdf = None

def word_to_pdf(input_path, output_path):
    """Helper function to convert DOC/DOCX to PDF using win32com."""
    try:
        import pythoncom
        import win32com.client
        
        pythoncom.CoInitialize()
        wdFormatPDF = 17 # Constant for PDF
        
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        
        abs_input = os.path.abspath(input_path)
        abs_output = os.path.abspath(output_path)
        
        doc = word.Documents.Open(abs_input)
        doc.SaveAs(abs_output, FileFormat=wdFormatPDF)
        doc.Close()
        word.Quit()
        return True
    except Exception as e:
        print(f"[Word COM Error] {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def convert_document(input_path, output_path, target_format):
    try:
        ext = os.path.splitext(input_path)[1].lower()
        target = target_format.lower()

        # 1. DOC/DOCX -> PDF
        if (ext == '.docx' or ext == '.doc') and target == 'pdf':
            return word_to_pdf(input_path, output_path)

        # 2. PDF -> DOCX
        elif ext == '.pdf' and target == 'docx':
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            return True

        # 3. PDF -> JPG/PNG
        elif ext == '.pdf' and (target == 'jpg' or target == 'png'):
            doc = fitz.open(input_path)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            pix.save(output_path)
            doc.close()
            return True

        # 4. DOC/DOCX -> JPG
        elif (ext == '.docx' or ext == '.doc') and target == 'jpg':
            temp_pdf = os.path.splitext(input_path)[0] + "_temp.pdf"
            if word_to_pdf(input_path, temp_pdf):
                doc = fitz.open(temp_pdf)
                page = doc.load_page(0)
                pix = page.get_pixmap()
                pix.save(output_path)
                doc.close()
                if os.path.exists(temp_pdf):
                    os.remove(temp_pdf)
                return True
            return False

        # 5. DOC -> DOCX
        elif ext == '.doc' and target == 'docx':
            temp_pdf = os.path.splitext(input_path)[0] + "_temp_conv.pdf"
            if word_to_pdf(input_path, temp_pdf):
                cv = Converter(temp_pdf)
                cv.convert(output_path, start=0, end=None)
                cv.close()
                if os.path.exists(temp_pdf):
                    os.remove(temp_pdf)
                return True
            return False

        return False

    except Exception as e:
        import traceback
        print(f"[Document Error] {str(e)}")
        traceback.print_exc()
        return False