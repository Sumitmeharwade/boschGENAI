from PyPDF2 import PdfReader
import fitz  # PyMuPDF
import os

def get_pdf_text(pdf_docs):
    try:
        text = ""
        pdf_reader = PdfReader(pdf_docs)
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"An error occurred while extracting text from PDF: {e}")
        return None

def extract_images_from_pdf(pdf_docs, output_folder="extracted_images"):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        pdf_document = fitz.open(stream=pdf_docs.read(), filetype="pdf")
        image_count = 0

        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            image_list = page.get_images(full=True)
            
            for image_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]

                image_filename = f"image_page{page_number + 1}_{image_index + 1}.png"
                image_filepath = os.path.join(output_folder, image_filename)

                with open(image_filepath, "wb") as image_file:
                    image_file.write(image_bytes)
                
                image_count += 1

        return image_count
    except Exception as e:
        print(f"An error occurred while extracting images from PDF: {e}")
        return None
