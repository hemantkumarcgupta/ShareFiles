import ocrmypdf
from PIL import Image
import os

def remove_alpha_channel(image_path):
    img = Image.open(image_path)
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        img = img.convert("RGB")
        temp_path = os.path.splitext(image_path)[0] + "_noalpha.jpg"
        img.save(temp_path, "JPEG")
        return temp_path
    return image_path

def make_ocr_pdf(input_file, overwrite=False, optimize=0):
    # Determine file type
    ext = os.path.splitext(input_file)[1].lower()
    
    # Only process images for alpha channel
    if ext in [".png", ".tif", ".tiff", ".bmp"]:
        input_file = remove_alpha_channel(input_file)
    
    # Prepare output file
    output_file = input_file if overwrite else os.path.splitext(input_file)[0] + "_ocr.pdf"
    
    # Run OCR
    ocrmypdf.ocr(
        input_file,
        output_file,
        force_ocr=True,
        deskew=True,
        image_dpi=300,
        optimize=optimize,
    )
    print(f"✅ OCR done: {output_file}")

# Examples
make_ocr_pdf("PDFTEST.pdf", overwrite=False, optimize=3)
make_ocr_pdf("PNGTEST.png", overwrite=False)
make_ocr_pdf("TIFTEST.tif", overwrite=False)