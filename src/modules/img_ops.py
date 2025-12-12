from PIL import Image

class ImageOps:
    @staticmethod
    def images_to_pdf(image_paths, output_path):
        try:
            if not image_paths:
                return False, "No images selected"
            
            images = []
            for path in image_paths:
                img = Image.open(path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)
            
            if images:
                images[0].save(output_path, save_all=True, append_images=images[1:])
                return True, f"Converted {len(image_paths)} images to {output_path}"
            return False, "No valid images processed"
        except Exception as e:
            return False, str(e)
