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
        
        # Ensure we use full normalized paths for Word COM
        abs_input = os.path.abspath(input_path).replace('/', '\\')
        abs_output = os.path.abspath(output_path).replace('/', '\\')
        
        print(f"[DOC] Attempting Word COM conversion: {abs_input} -> {abs_output}")
        
        if not os.path.exists(abs_input):
            print(f"[DOC Error] Input file missing for Word: {abs_input}")
            return False

        pythoncom.CoInitialize()
        wdFormatPDF = 17 # Constant for PDF
        
        # Use DispatchEx to ensure a fresh instance
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0 # wdAlertsNone
        
        try:
            doc = word.Documents.Open(abs_input, ReadOnly=True)
            doc.SaveAs(abs_output, FileFormat=wdFormatPDF)
            doc.Close(0) # wdDoNotSaveChanges
            success = True
        except Exception as e:
            print(f"[Word Open/Save Error] {str(e)}")
            success = False
        finally:
            word.Quit()
            pythoncom.CoUninitialize()
            
        return success
    except Exception as e:
        print(f"[Word COM Critical Error] {str(e)}")
        return False

def convert_document(input_path, output_path, target_format, preset_params=None):
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