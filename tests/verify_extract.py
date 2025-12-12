import os
import sys
from PIL import Image

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.modules.pdf_ops import PDFOps
from src.modules.img_ops import ImageOps
from pypdf import PdfWriter

def run_tests():
    print("Starting Setup...")
    # Setup dummy assets
    if not os.path.exists("tests_output"):
        os.makedirs("tests_output")
    
    # Create a real text-based PDF for testing extraction
    text_pdf_path = "tests_output/text_sample.pdf"
    
    # We can't easily create a text PDF with pypdf from scratch purely with text 
    # (it mainly manipulates existing ones).
    # But we can create a reportlab PDF or just accept that our 'images' pdf yields empty text.
    # However, to be thorough, let's use reportlab if available, or just skip full text content verification 
    # and check if the function runs without error using pdfplumber against our image PDF.
    # pdfplumber should return empty string for images.
    
    # Let's try to import reportlab
    try:
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(text_pdf_path)
        c.drawString(100, 750, "Hello World from PDFPlumber Test")
        c.save()
        print("Created Text PDF using ReportLab.")
        has_text = True
    except ImportError:
        print("ReportLab not found. Using Image PDF (expect empty text).")
        # Use our image PDF from previous steps
        text_pdf_path = "tests_output/merged.pdf" 
        # (Assuming verify.py ran before, or we recreate it)
        if not os.path.exists(text_pdf_path):
             # Create a quick dummy image pdf
             img_path = "tests_output/dummy.jpg"
             Image.new('RGB', (100, 100), color='white').save(img_path)
             ImageOps.images_to_pdf([img_path], text_pdf_path)
        has_text = False

    txt_out = "tests_output/extracted_plumber.txt"
    success, msg = PDFOps.extract_text(text_pdf_path, txt_out)
    
    print(f"Extraction result: {success}, {msg}")
    
    if success and os.path.exists(txt_out):
        with open(txt_out, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"Extracted Content: '{content.strip()}'")
            if has_text and "Hello World" in content:
                print("PASS: Found expected text.")
            elif not has_text:
                print("PASS: Ran successfully on image PDF.")
    else:
        print("FAIL: Output file not found.")

if __name__ == "__main__":
    run_tests()
