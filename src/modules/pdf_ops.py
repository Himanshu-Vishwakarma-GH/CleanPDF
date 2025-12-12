import os
from pypdf import PdfReader, PdfWriter

class PDFOps:
    @staticmethod
    def merge_pdfs(input_paths, output_path):
        try:
            merger = PdfWriter()
            for path in input_paths:
                merger.append(path)
            merger.write(output_path)
            merger.close()
            return True, f"Merged {len(input_paths)} files to {output_path}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def split_pdf(input_path, output_dir, page_range=None):
        try:
            reader = PdfReader(input_path)
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            total_pages = len(reader.pages)
            
            # Determine pages to export
            pages_to_export = set()
            if page_range:
                # Parse range "1-3,5, 8-10"
                parts = [p.strip() for p in page_range.split(',')]
                for part in parts:
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        # Adjust to 0-based, handle inclusive range
                        for p in range(start - 1, end):
                            if 0 <= p < total_pages:
                                pages_to_export.add(p)
                    else:
                        p = int(part) - 1
                        if 0 <= p < total_pages:
                            pages_to_export.add(p)
            else:
                # All pages
                pages_to_export = set(range(total_pages))
            
            if not pages_to_export:
                 return False, "No valid pages to split."

            count = 0
            for i in sorted(list(pages_to_export)):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                output_filename = f"{base_name}_page_{i+1}.pdf"
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, "wb") as out_file:
                    writer.write(out_file)
                count += 1
            
            return True, f"Split into {count} files in {output_dir}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    @staticmethod
    def compress_pdf(input_path, output_path, level="medium"):
        try:
            # Reverting to pypdf because pymupdf causes PyInstaller issues in this env.
            # pypdf compresses by default on write.
            # We can also attempt to reduce file size by removing duplication.
            
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            # Additional optimization flags if available in newer pypdf
            for page in writer.pages:
                page.compress_content_streams() # Ensure streams are compressed
            
            # Level handling: pypdf is limited. We just do standard compression.
            # (In a real scenario, we might use Ghostscript but that requires external install)
            
            with open(output_path, "wb") as f:
                writer.write(f)
                
            return True, f"Compressed (Standard) and saved to {output_path}"
        except Exception as e:
            return False, f"Compression error: {str(e)}"

    @staticmethod
    def extract_text(input_path, output_path):
        try:
            reader = PdfReader(input_path)
            text_content = []
            
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    text_content.append(f"--- Page {i+1} ---\n{text}\n")
            
            total_chars = sum(len(t) for t in text_content)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(text_content))
            
            if total_chars < 10:
                return True, f"Warning: Only {total_chars} chars extracted. Document might be an image. Saved to {output_path}"
                
            return True, f"Extracted text from {len(text_content)} pages to {output_path}"
        except Exception as e:
            return False, f"Extraction error: {str(e)}"

    @staticmethod
    def encrypt_pdf(input_path, output_path, password):
        try:
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            writer.encrypt(password)
            
            with open(output_path, "wb") as f:
                writer.write(f)
            return True, f"Encrypted and saved to {output_path}"
        except Exception as e:
            return False, f"Encryption failed: {str(e)}"

    @staticmethod
    def decrypt_pdf(input_path, output_path, password):
        try:
            reader = PdfReader(input_path)
            
            if reader.is_encrypted:
                reader.decrypt(password)
            
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
                
            with open(output_path, "wb") as f:
                writer.write(f)
            return True, f"Decrypted and saved to {output_path}"
        except Exception as e:
            return False, f"Decryption failed: {str(e)}"
    
    @staticmethod
    def organize_pages(input_path, output_path, page_config):
        """
        page_config: List of dicts [{'index': int, 'rotate': int}]
        """
        try:
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            # Reorder and Rotate
            for item in page_config:
                idx = item.get('index')
                rotation = item.get('rotate', 0)
                
                if 0 <= idx < len(reader.pages):
                    page = reader.pages[idx]
                    if rotation != 0:
                        page.rotate(rotation)
                    writer.add_page(page)
            
            with open(output_path, "wb") as f:
                writer.write(f)
            return True, f"Organized PDF saved to {output_path}"
        except Exception as e:
            return False, f"Organize failed: {str(e)}"
