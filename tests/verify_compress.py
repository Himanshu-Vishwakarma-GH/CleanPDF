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
    
    # Create large dummy image to see compression
    img_path = "tests_output/large.jpg"
    # Create a 2000x2000 image with noise to ensure some size
    import random
    
    # Simple large image
    Image.new('RGB', (2000, 2000), color='blue').save(img_path)
    
    pdf_path = "tests_output/large.pdf"
    ImageOps.images_to_pdf([img_path], pdf_path)
    
    orig_size = os.path.getsize(pdf_path)
    print(f"Created PDF: {orig_size} bytes")

    # Test Compression (Levels ignored in pypdf fallback, but API exists)
    for level in ["low", "medium", "high"]:
        out_path = f"tests_output/compressed_{level}.pdf"
        success, msg = PDFOps.compress_pdf(pdf_path, out_path, level)
        if success:
            new_size = os.path.getsize(out_path)
            ratio = 100 * (orig_size - new_size) / orig_size
            print(f"[{level.upper()}] Success: {new_size} bytes (Reduced {ratio:.2f}%)")
        else:
            print(f"[{level.upper()}] Failed: {msg}")

if __name__ == "__main__":
    run_tests()
