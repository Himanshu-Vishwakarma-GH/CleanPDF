import os
import sys
from PIL import Image

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.modules.pdf_ops import PDFOps
from src.modules.img_ops import ImageOps

def run_tests():
    print("Starting Setup...")
    # Setup dummy assets
    if not os.path.exists("tests_output"):
        os.makedirs("tests_output")
    
    img1_path = "tests_output/test1.jpg"
    img2_path = "tests_output/test2.jpg"
    
    Image.new('RGB', (100, 100), color='red').save(img1_path)
    Image.new('RGB', (100, 100), color='blue').save(img2_path)
    print("Created dummy images.")

    # 1. Test Images to PDF
    print("\n[1] Testing Images to PDF...")
    pdf1_path = "tests_output/img_pdf1.pdf"
    pdf2_path = "tests_output/img_pdf2.pdf"
    
    success, msg = ImageOps.images_to_pdf([img1_path], pdf1_path)
    print(f"Img->PDF 1: {success}, {msg}")
    
    success, msg = ImageOps.images_to_pdf([img2_path], pdf2_path)
    print(f"Img->PDF 2: {success}, {msg}")
    
    if not (os.path.exists(pdf1_path) and os.path.exists(pdf2_path)):
        print("FAIL: PDFs not created")
        return

    # 2. Test Merge
    print("\n[2] Testing Merge PDF...")
    merged_path = "tests_output/merged.pdf"
    success, msg = PDFOps.merge_pdfs([pdf1_path, pdf2_path], merged_path)
    print(f"Merge: {success}, {msg}")
    
    if not os.path.exists(merged_path):
        print("FAIL: Merged PDF not created")
        return

    # 3. Test Split
    print("\n[3] Testing Split PDF...")
    split_dir = "tests_output/split"
    if not os.path.exists(split_dir):
        os.makedirs(split_dir)
        
    success, msg = PDFOps.split_pdf(merged_path, split_dir)
    print(f"Split: {success}, {msg}")
    
    # Expect 2 pages
    split_files = os.listdir(split_dir)
    print(f"Split files found: {split_files}")
    if len(split_files) < 2:
        print("FAIL: Did not split into 2 files")

    # 4. Test Compress (Repack)
    print("\n[4] Testing Compress PDF...")
    compressed_path = "tests_output/compressed.pdf"
    success, msg = PDFOps.compress_pdf(merged_path, compressed_path)
    print(f"Compress: {success}, {msg}")
    if not os.path.exists(compressed_path):
        print("FAIL: Compressed PDF not created")

    # 5. Test Extract Text
    print("\n[5] Testing Extract Text...")
    # Note: Our Image PDFs have no text, so this should run but return empty string presumably
    text_path = "tests_output/extracted.txt"
    success, msg = PDFOps.extract_text(merged_path, text_path)
    print(f"Extract: {success}, {msg}")
    if not os.path.exists(text_path):
        print("FAIL: Text file not created")
    else:
        with open(text_path, 'r') as f:
            content = f.read()
            print(f"Extracted Content Length: {len(content)} (Expected 0 or low for images)")

    print("\nDone. Check tests_output directory.")

if __name__ == "__main__":
    run_tests()
