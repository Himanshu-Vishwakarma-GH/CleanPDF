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
    
    # Create 5 dummy images to make a 5-page PDF
    img_paths = []
    colors = ['red', 'blue', 'green', 'yellow', 'black']
    for i, color in enumerate(colors):
        p = f"tests_output/p{i+1}.jpg"
        Image.new('RGB', (100, 100), color=color).save(p)
        img_paths.append(p)

    # Make 5-page PDF
    merged_path = "tests_output/5pages.pdf"
    ImageOps.images_to_pdf(img_paths, merged_path)
    print("Created 5-page PDF.")

    # Test Split All
    print("\n[1] Testing Split All...")
    split_dir_all = "tests_output/split_all"
    if not os.path.exists(split_dir_all):
        os.makedirs(split_dir_all)
    
    success, msg = PDFOps.split_pdf(merged_path, split_dir_all)
    print(f"Split All: {success}, {msg}")
    if len(os.listdir(split_dir_all)) != 5:
        print("FAIL: Expected 5 files")

    # Test Split Range "1-2, 4"
    print("\n[2] Testing Split Range '1-2, 4' (Expected pages 1, 2, 4)...")
    split_dir_range = "tests_output/split_range"
    if not os.path.exists(split_dir_range):
        os.makedirs(split_dir_range)
    
    success, msg = PDFOps.split_pdf(merged_path, split_dir_range, "1-2, 4")
    print(f"Split Range: {success}, {msg}")
    
    files = sorted(os.listdir(split_dir_range))
    print(f"Files: {files}")
    # Expected: 5pages_page_1.pdf, 5pages_page_2.pdf, 5pages_page_4.pdf
    if len(files) == 3 and "5pages_page_4.pdf" in files:
        print("PASS: Range split successful")
    else:
        print("FAIL: Range split failed")

if __name__ == "__main__":
    run_tests()
